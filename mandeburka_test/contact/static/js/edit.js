var ajaxInProcess = false;
var patt = new RegExp('{{ MEDIA_URL }}');
$(function() {
    $('#edit_form').submit(function(e){
        e.preventDefault();
        if (ajaxInProcess){
            return false;
        }
        ajaxInProcess = true;
        var $form = $(this);
        var data = $form.serialize();
        $form.find('input, textarea').attr('disabled', 'disabled');
        $('#spinner').show();
        $('#success').hide();
        $.post('/edit', data, function(data){
            $('#spinner').hide();
            ajaxInProcess = false;
            $form.find('input, textarea').removeAttr('disabled');
            if (typeof data.errors != 'undefined') {
                var msg = 'Invalid fields:\n';
                $.each(data.errors, function(i, e){
                    msg += $('label[for="id_' + i + '"]').text().replace(/:$/, '') + '\n';
                });
                alert(msg);
            } else {
                $('#success').show();
            }
        });
    });
    var uploader = new qq.FileUploader({
        action: "{% url contact:my_ajax_upload %}",
        element: $('#file-uploader')[0],
        multiple: false,
        onComplete: function(id, fileName, responseJSON) {
            if(responseJSON.success) {
                $('.photo-preview').attr('src', responseJSON.path);
                $('#id_photo').val(responseJSON.path.replace(patt, ''));
            } else {
                alert("upload failed!");
            }
        },
        onAllComplete: function(uploads) {
        // uploads is an array of maps
        // the maps look like this: {file: FileObject, response: JSONServerResponse}
        },
        params: {
            'csrf_token': '{{ csrf_token }}',
            'csrf_name': 'csrfmiddlewaretoken',
            'csrf_xname': 'X-CSRFToken'
        }
    });
});
