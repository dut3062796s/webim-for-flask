/*!
 * WebIM for Flask @VERSION
 * http://nextalk.im
 *
 * Copyright (c) 2013 NexTalk.IM
 *
 * Released under the MIT, BSD, and GPL Licenses.
 */
(function(webim) {
	var path = _IMC.path;
	webim.extend(webim.setting.defaults.data, _IMC.setting);
	var webim = window.webim;
	//configure api routes
	webim.route( {
		online: path + "/webim/online",
		offline: path + "/webim/offline",
		deactivate: path + "/webim/refresh",
		message: path + "/webim/message",
		presence: path + "/webim/presence",
		status: path + "/webim/status",
		setting: path + "/webim/setting",
		history: path + "/webim/history",
		clear: path + "/webim/history/clear",
		download: path + "/webim/history/download",
		members: path + "/webim/members",
		join: path + "/webim/group/join",
		leave: path + "/webim/group/leave",
		buddies: path + "/webim/buddies",
		notifications: path + "/webim/notifications"
	} );

	//configure emotion icons
	webim.ui.emot.init({"dir": path + "/static/webim/images/emot/default"});

	//configure sound mp3
	var soundUrls = {
		lib: path + "/static/webim/assets/sound.swf",
		msg: path + "/static/webim/assets/sound/msg.mp3"
	};

	//configure ui
	var ui = new webim.ui(document.body, {
		imOptions: {
			jsonp: _IMC.jsonp
		},
		soundUrls: soundUrls,
		buddyChatOptions: {
            downloadHistory: !_IMC.is_visitor,
			simple: _IMC.is_visitor,
			upload: _IMC.upload && !_IMC.is_visitor
		},
		roomChatOptions: {
			upload: _IMC.upload
		}
	}), im = ui.im;

	if( _IMC.user ) im.setUser( _IMC.user );
	if( _IMC.menu ) ui.addApp("menu", { "data": _IMC.menu } );
	if( _IMC.enable_shortcut ) ui.layout.addShortcut( _IMC.menu );

	//configure buddy list
	ui.addApp("buddy", {
		showUnavailable: _IMC.show_unavailable,
		is_login: _IMC['is_login'],
		disable_login: true,
		collapse: false,
		disable_user: _IMC.is_visitor,
        simple: _IMC.is_visitor,
		loginOptions: _IMC['login_options']
	} );
    if(!_IMC.is_visitor) {
        //room button
        if( _IMC.enable_room )ui.addApp("room", { discussion: false});
        //notification button
        if( _IMC.enable_noti )ui.addApp("notification");
    }
    //setting button
    ui.addApp("setting", {"data": webim.setting.defaults.data});
    //render
	ui.render();
	//online
	_IMC['is_login'] && im.autoOnline() && im.online();
})(webim);

