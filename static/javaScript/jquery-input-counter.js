jQuery.fn.inputCounter = function (options) {

    var defaults = {
        selectors: {
            addButtonSelector: '.btn-add',
            subtractButtonSelector: '.btn-subtract',
            inputSelector: '.input-counter',
        },
        settings: {
            checkValue: true,
            isReadOnly: true,
        },
    };

    var settings = $.extend({}, defaults, options);

    var methods = {
        init: function (element) {
            var me = this;

            methods.registerEvents(element);
            methods.initInput(element);
        },

        initInput: function (element) {
            var me = this;
            var defaultValue = $(element).find(settings.selectors.inputSelector).data("default");

            // the default value
            $(element).find(settings.selectors.inputSelector).val(defaultValue);

            // set readonly-value
            if(settings.settings.isReadOnly == true) {
                $(element).find(settings.selectors.inputSelector).prop('readonly', true);
            } else {
                $(element).find(settings.selectors.inputSelector).prop('readonly', false);
            }
        },

        registerEvents: function (element) {
            var me = this;
            var addButtonElement = $($(element).find(settings.selectors.addButtonSelector)[0]);
            var subtractButtonElement = $($(element).find(settings.selectors.subtractButtonSelector)[0]);
            var input = $($(element).find(settings.selectors.inputSelector)[0]);

            addButtonElement.on("click touchstart", $.proxy(me.onAddButtonClicked, me, element));
            subtractButtonElement.on("click touchstart", $.proxy(me.onSubtractButtonClicked, me, element));
            input.on("focusout", $.proxy(me.onInputFocusOut, me, element));
        },

        onAddButtonClicked: function (element) {
            var me = this;
            var input = $($(element).find(settings.selectors.inputSelector)[0]);

            var newValue = (parseInt(input.val()) + 1);

            me.setValue(element, parseInt(input.val()), newValue);
        },

        onSubtractButtonClicked: function (element) {
            var me = this;
            var input = $($(element).find(settings.selectors.inputSelector)[0]);

            var newValue = (parseInt(input.val()) - 1);

            me.setValue(element, parseInt(input.val()), newValue);
        },

        onInputFocusOut: function (element) {
            var me = this;
            var input = $($(element).find(settings.selectors.inputSelector)[0]);
            var minValue = input.data("min");
            var maxValue = input.data("max");

            var newValue = parseInt(input.val());

            if(me.checkValue(element, newValue) == -1) {
                input.val(minValue);
            } else if(me.checkValue(element, newValue) == -2) {
                input.val(maxValue);
            }
        },

        setValue: function (element, oldValue, newValue)  {
            var me = this;
            var input = $($(element).find(settings.selectors.inputSelector)[0]);

            if(me.checkValue(element, newValue) == true) {
                input.val(newValue);
                input.trigger('propertychange');
            } else {
                input.val(oldValue);
                input.trigger('propertychange');
            }
        },

        checkValue: function (element, newValue) {
            var me = this;
            var input = $($(element).find(settings.selectors.inputSelector)[0]);
            var minValue = input.data("min");
            var maxValue = input.data("max");

            if(settings.settings.checkValue != true) {
                return true;
            }

            if (minValue == undefined && maxValue == undefined) {
                return true;
            } else if (minValue == undefined && maxValue != undefined && newValue <= parseInt(maxValue)) {
                return true;
            } else if (maxValue == undefined && minValue != undefined && newValue >= parseInt(minValue)) {
                return true;
            } else if (maxValue != undefined && minValue != undefined && newValue >= parseInt(minValue) && newValue <= parseInt(maxValue)) {
                return true;
            } else {
                if(newValue < parseInt(minValue)) {
                    // to low
                    return -1;
                } else if (newValue > parseInt(maxValue)) {
                    // to large
                    return -2;
                }
            }
        },
    };

    return this.each(function () {
        methods.init($(this));
    });
};