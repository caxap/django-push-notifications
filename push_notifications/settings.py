from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

__all__ = ['DEFAULT_APP_ALIAS', 'PUSH_NOTIFICATIONS_SETTINGS', 'get_gcm_settings', 'get_apns_settings']


DEFAULT_APP_ALIAS = 'default'

if getattr(settings, 'DEBUG', False):
	DEFAULT_APNS_HOST = 'gateway.sandbox.push.apple.com'
else:
	DEFAULT_APNS_HOST = 'gateway.push.apple.com'

DEFAULTS = {
	'APNS_APPS': {},
	'APNS_PORT': 2195,
	'APNS_HOST': DEFAULT_APNS_HOST,
	'GCM_APPS': {},
	'GCM_POST_URL': 'https://android.googleapis.com/gcm/send',
	'GCM_MAX_RECIPIENTS': 1000,
}

PUSH_NOTIFICATIONS_SETTINGS = getattr(settings, "PUSH_NOTIFICATIONS_SETTINGS", {})
PUSH_NOTIFICATIONS_SETTINGS.update(dict(DEFAULTS, **PUSH_NOTIFICATIONS_SETTINGS))


def _get_app_settings(app_setting_name, app_name=None):
	"""
	These function collapse complex settings structure for giver app name.
	So all other code still using same settings format.
	"""
	if app_name is None:
		app_name = DEFAULT_APP_ALIAS

	conf = dict(PUSH_NOTIFICATIONS_SETTINGS)
	app_conf = conf.pop(app_setting_name, {}).get(app_name)
	if not app_conf and app_name != DEFAULT_APP_ALIAS:
		raise ImproperlyConfigured(
			"{0}['{1}'] has not beed configured".format(app_setting_name, app_name))
	if app_conf:
		conf.update(app_conf)
	return conf


def get_gcm_settings(app_name=DEFAULT_APP_ALIAS):
	conf = _get_app_settings('GCM_APPS', app_name)
	# Back compatibility check for default GCM app
	if not conf.get('GCM_API_KEY'):
		raise ImproperlyConfigured(
			"PUSH_NOTIFICATIONS_SETTINGS['GCM_API_KEY'] has not beed configured")
	return conf


def get_apns_settings(app_name=DEFAULT_APP_ALIAS):
	conf = _get_app_settings('APNS_APPS', app_name)
	# Back compatibility check for default APN app_name
	if not conf.get('APNS_CERTIFICATE'):
		raise ImproperlyConfigured(
			"PUSH_NOTIFICATIONS_SETTINGS['APNS_CERTIFICATE'] has not beed configured")
	return conf
