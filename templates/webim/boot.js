//
//TODO: FIXME Later
//
var _IMC = {
	version: 'v5',
	path: '',
	is_login: '1',
    is_visitor: {{ WEBIM_CFG.is_visitor|tojson }},
	login_options: "",
	user: '',
	setting: {{ WEBIM_CFG.setting|tojson }},
	menu: "",
	enable_chatbtn: true,
	enable_chatlink: {{ WEBIM_CFG.enable_chatlink|tojson }},
	enable_shortcut: {{ WEBIM_CFG.enable_shortcut|tojson }},
	enable_menu: '',
	discussion: {{ WEBIM_CFG.discussion|tojson }},
	enable_room: {{ WEBIM_CFG.enable_room|tojson }},
	enable_noti: {{ WEBIM_CFG.enable_noti|tojson }},
	theme: '{{ WEBIM_CFG.theme }}',
	local: '{{ WEBIM_CFG.local }}',
	upload: {{ WEBIM_CFG.upload|tojson }},
	show_unavailable: {{ WEBIM_CFG.show_unavailable|tojson }},
	jsonp: '',
	min: ''
};

_IMC.script = window.webim ? '' : ('<link href="' + _IMC.path + '/static/webim/webim' + _IMC.min + '.css?' + _IMC.version + '" media="all" type="text/css" rel="stylesheet"/><link href="' + _IMC.path + '/static/webim/themes/' + _IMC.theme + '/jquery.ui.theme.css?' + _IMC.version + '" media="all" type="text/css" rel="stylesheet"/><script src="' + _IMC.path + '/static/webim/webim' + _IMC.min + '.js?' + _IMC.version + '" type="text/javascript"></script><script src="' + _IMC.path + '/static/webim/i18n/webim-' + _IMC.local + '.js?' + _IMC.version + '" type="text/javascript"></script>');
_IMC.script += '<script src="' + _IMC.path + '/static/webim/webim.flask.js?' + _IMC.version + '" type="text/javascript"></script>';

document.write( _IMC.script );

