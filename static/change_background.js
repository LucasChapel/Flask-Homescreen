

function readImage() {
    var image = document.getElementById('file-upload').files[0];

    if(image.size > 5242880){
        alert("Le fichier selectionné est trop volumineux");
        image.value = "";
    }else{
        var output = document.getElementById('output');
        var reader = new FileReader();
        reader.addEventListener('load', (event) => {
            output.src = event.target.result;
            document.getElementById('output').style.visibility = "visible";
            localStorage.setItem("image_background", output.src);
        });
        reader.readAsDataURL(image);
        change_bg("white")
    };
};

window.onload = function() {
    set_background();
};

function set_background(){
    var image = localStorage.getItem("image_background");
    if (image){
        document.getElementById('output').src = image;
        document.getElementById('output').style.visibility = "visible";
        change_bg("white");
        
    } else{
        retour_fond();
    }
    
};

function change_bg(color){
    document.body.style.background = color;
};

function retour_fond(){
    localStorage.setItem("image_background", "");
    document.getElementById('output').style.visibility = "hidden";
    document.body.style.background = "lightsalmon";
}