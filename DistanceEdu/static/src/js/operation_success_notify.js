openerp.DistanceEdu = function(instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.DistanceEdu.operationsuccess = instance.web.Widget.extend({
        init: function(parent,action){
            this._super(parent, action);
            this.action = action;
        },
        start: function () {
            var self = this;
            self.do_notify(_t(self.action.action.message.title), _t(self.action.action.message.message));
            history.go(-1);
            //self.view.reload();
            //return {'type':'ir.actions.act_window_close'};
        },
        doNotify: function(message){
            var self=this;
            self.do_notify(_t(message.title), _t(message.message));
        }
    });

    instance.web.client_actions.add("operation_success", "instance.DistanceEdu.operationsuccess");
}
odoo.define('distanceedu.donotify', function (require) {
    "use strict";
var core = require('web.core');
//var listview = require('web.list_view');
core.action_registry.add('action_notify', function(element, action){
    var params = action.params;
    if(params){
        element.do_notify(params.title, params.text, params.sticky);

    }
    return {'type':'ir.actions.act_window_close'};

});
});
