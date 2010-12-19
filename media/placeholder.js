var MyApp = {

	addPlaceholders: function(props) {

		// default configuration
		var config = {
			'class': 'placeholder' // apply CSS classes to an input displaying a placeholder
		};

		// if any properties were supplied, apply them to the config object
		for (var key in props) {
			if (config.hasOwnProperty(key)) {
				config[key] = props[key];
			}
		}

		// create a basic form for testing support
		var testform = $('<form><input type="text"></form>');

		// extend jQuery.support() for testing "placeholder" attribute support
		$.extend($.support, {
			placeHolder: !!($('input', testform)[0].placeholder !== undefined || $('input', testform)[0].placeHolder !== undefined)
		});

		// create placeholders by using "value" attribute
		if (!$.support.placeHolder) {
			$('input[placeholder]').each(function() {
				var placeholder = $(this).attr('placeholder');
				$(this).bind({
					'focus': function() {
						if ($(this).val() === placeholder) {
							$(this).val('');
                            $(this).removeClass(config['class']);
                            // $(this).removeClass('notnative');
						}
						$(this).attr('data-focused', 'yes');
					},
					'blur': function() {
						if ($(this).val() === '') {
                            $(this).val(placeholder);
                            $(this).addClass(config['class']);
                            $(this).addClass('notnative');
						}
						$(this).removeAttr('data-focused');
					}
				});
				// only add placeholder on load when value is empty or placeholder or input is not focused (focus is preserved while reloading/XHR)
				if ((($(this).val() === '') || ($(this).val() === placeholder)) && (!$(this).attr('data-focused'))) {
                    $(this).val(placeholder);
                    $(this).addClass(config['class']);
                    $(this).addClass('notnative');
				}
			});
		}

	}

};

$(document).ready(function() {
	MyApp.addPlaceholders();
});