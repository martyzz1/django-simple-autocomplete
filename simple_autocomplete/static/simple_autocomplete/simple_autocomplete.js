 (function($) {
    $(document).ready(function() {

        $(document).on('keydown.autocomplete', '.sa_autocompletewidget',  function(){
            console.log($(this).attr('data-url'));
            var url = $(this).attr('data-url');
            $(this).autocomplete({
                source: function(request, response){
                    $.ajax({
                        url: url,
                        data: {q: request.term},
                        success: function(data) {
                            if (data != 'CACHE_MISS')
                            {
                                response($.map(data, function(item) {
                                    return {
                                        label: item[1],
                                        value: item[1],
                                        real_value: item[0]
                                    };
                                }));
                            }
                        },
                        dataType: "json"
                    });
                },
                select: function(event, ui) { $(this).nextAll('input').first().val(ui.item.real_value); },
                minLength: 3
            });
        });

        $(document).on('keydown.autocomplete', '.sa_autocompletemultiplewidget',  function(){
            console.log($(this).attr('data-url'));
            var url = $(this).attr('data-url');
            var name = $(this).attr('data-name');
            var id = $(this).id;
            $(this).autocomplete({
                source: function(request, response) {
                    $.ajax({
                        url: url,
                        data: {q: request.term},
                        success: function(data) {
                            if (data != 'CACHE_MISS')
                            {
                                response($.map(data, function(item) {
                                    return {
                                        label: item[1],
                                        value: item[1],
                                        real_value: item[0]
                                    };
                                }));
                            }
                        },
                        dataType: "json"
                    });
                },
                select: function(event, ui) {
                    var parent = $(this).parent();
                    var target = $('div.autocomplete-placeholder', parent);
                    target.append('<p><input name="' + name + '" value="' + ui.item.real_value + '" '
                        + 'type="hidden" />' + ui.item.value
                        + ' <a href="#" title="Remove" onclick="django.jQuery(this).parent().remove(); django.jQuery('+"'"+id+"'"+').val(' + "''" + '); django.jQuery('+"'"+id+"'"+').focus(); return false;">x<small></small></a></p>');
                },
                close: function(event, ui) {
                    $(this).val('');
                },
                minLength: 3
            });
        });
    });

})(django.jQuery);

