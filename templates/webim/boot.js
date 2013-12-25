//
//TODO: FIXME Later
//
var _IMC = {
	version: 'v5.2',
	path: '{{ urlpath }}',
	is_login: '1',
	login_options: "",
	user: '',
	setting: {},
	menu: "",
	enable_chatlink: {{ WEBIM_CFG.ENABLE_CHATLINK|tojson }},
	enable_shortcut: {{ WEBIM_CFG.ENABLE_SHORTCUT|tojson }},
	enable_menu: '',
	enable_room: {{ WEBIM_CFG.ENABLE_ROOM|tojson }},
	enable_noti: {{ WEBIM_CFG.ENABLE_NOTI|tojson }},
	theme: '{{ WEBIM_CFG.THEME }}',
	local: '{{ WEBIM_CFG.LOCAL }}',
	upload: {{ WEBIM_CFG.UPLOAD|tojson }},
	show_unavailable: {{ WEBIM_CFG.SHOW_UNAVAILABLE|tojson }},
	jsonp: '',
	min: ''
};

_IMC.script = window.webim ? '' : ('<link href="' + _IMC.path + '/static/webim/webim' + _IMC.min + '.css?' + _IMC.version + '" media="all" type="text/css" rel="stylesheet"/><link href="' + _IMC.path + '/static/webim/themes/' + _IMC.theme + '/jquery.ui.theme.css?' + _IMC.version + '" media="all" type="text/css" rel="stylesheet"/><script src="' + _IMC.path + '/static/webim/webim' + _IMC.min + '.js?' + _IMC.version + '" type="text/javascript"></script><script src="' + _IMC.path + 'static/webim/i18n/webim-' + _IMC.local + '.js?' + _IMC.version + '" type="text/javascript"></script>');
_IMC.script += '<script src="' + _IMC.path + '/static/webim.flask.js?' + _IMC.version + '" type="text/javascript"></script>';

document.write( _IMC.script );

