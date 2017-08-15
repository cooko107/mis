/**
 * Created by CK on 2017/4/6.
 */
odoo.define('finance.hideedit', function (require) {
    "use strict";
var FormView = require('web.FormView');
FormView.include({
    do_push_state: function() {
        this._super.apply(this, arguments);
        if (this.options.action != null){
            var no_edit = this.options.action.context.form_no_edit;
            if(no_edit!=undefined){
                var result = this.compute_domain(no_edit);
                if(result==true){
                    if(this.get("actual_mode")!="view"){
                        this.$buttons.find('.oe_form_button_cancel').trigger('click')
                    }
                    this.$buttons.find(".oe_form_button_edit").hide();
                }else{
                    if(this.get("actual_mode")=="view") {
                        this.$buttons.find(".oe_form_button_edit").show();
                    }
                }
            }
        }
    }
});
});

