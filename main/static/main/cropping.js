$(function () {

    /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
    $("#id_profile_picture").change(function () {
         
    if (this.files && this.files[0]) {
        const file_size = (this.files[0].size / 1024 / 1024).toFixed(2); 
  
        if (file_size > 1) { 
            alert("File size must be less than 1 MB"); 
        } 
        
        else { 
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#image").attr("src", e.target.result);
                $("#modalCrop").modal({
                    backdrop: 'static', 
                    keyboard: false
                });
            }
            reader.readAsDataURL(this.files[0]);
        } 
    }
});

/* SCRIPTS TO HANDLE THE CROPPER BOX */
var $image = $("#image");
var cropBoxData;
var canvasData;
$("#modalCrop").on("shown.bs.modal", function () {
    $image.cropper({
        viewMode: 1,
        aspectRatio: 1/1,
        minCropBoxWidth: 200,
        minCropBoxHeight: 200,
        ready: function () {
            $image.cropper("setCanvasData", canvasData);
            $image.cropper("setCropBoxData", cropBoxData);
        }
    });
}).on("hidden.bs.modal", function () {
    cropBoxData = $image.cropper("getCropBoxData");
    canvasData = $image.cropper("getCanvasData");
    $image.cropper("destroy");
});

$(".js-zoom-in").click(function () {
    $image.cropper("zoom", 0.1);
});

$(".js-zoom-out").click(function () {
    $image.cropper("zoom", -0.1);
});

/* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
$(".js-crop-and-upload").click(function () {
    var cropData = $image.cropper("getData");
    $("#id_x").val(cropData["x"]);
    $("#id_y").val(cropData["y"]);
    $("#id_height").val(cropData["height"]);
    $("#id_width").val(cropData["width"]);
    $("#id_user_form").submit();
    });
});