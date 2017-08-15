
openerp.DistanceEdu = function(instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.DistanceEdu.importfail = instance.web.Widget.extend({
        init: function(parent,action){
            this._super(parent, action);
            this.action = action;
        },
        start: function () {
            var self = this;
            self.do_warn(_t(self.action.action.message.title), _t(self.action.action.message.message));
        },
        doWarn: function(message){
            var self=this;
            self.do_warn(_t(message.title), _t(message.message));
        }
    });

    instance.web.client_actions.add("importfail", "instance.DistanceEdu.importfail");
}