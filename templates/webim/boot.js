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
	enable_chatlink: false,
	enable_shortcut: false,
	enable_menu: '',
	enable_room: true,
	enable_noti: true,
	theme: 'blitzer',
	local: 'zh-CN',
	upload: true,
	show_unavailable: true,
	jsonp: '',
	min: ''
};

_IMC.script = window.webim ? '' : ('<link href="' + _IMC.path + '/static/webim/webim' + _IMC.min + '.css?' + _IMC.version + '" media="all" type="text/css" rel="stylesheet"/><link href="' + _IMC.path + '/static/webim/themes/' + _IMC.theme + '/jquery.ui.theme.css?' + _IMC.version + '" media="all" type="text/css" rel="stylesheet"/><script src="' + _IMC.path + '/static/webim/webim' + _IMC.min + '.js?' + _IMC.version + '" type="text/javascript"></script><script src="' + _IMC.path + 'static/webim/i18n/webim-' + _IMC.local + '.js?' + _IMC.version + '" type="text/javascript"></script>');
_IMC.script += '<script src="' + _IMC.path + '/static/webim.flask.js?' + _IMC.version + '" type="text/javascript"></script>';

document.write( _IMC.script );

