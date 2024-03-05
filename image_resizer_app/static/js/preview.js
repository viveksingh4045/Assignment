    // Range preview function

    function previewRange() {
      var rangeValue = document.getElementById('range').value;
      document.querySelector('.range-preview').textContent = "Selected resizing factor: " + rangeValue +"%";
    }

    // Image preview function
    function previewImages() {
      var preview = document.querySelector('.image-preview');
      var files = document.querySelector('input[type=file]').files;
      preview.innerHTML = '';
      var h4 = document.createElement("h4");
      var textNode = document.createTextNode("Preview: ");
      h4.appendChild(textNode);
      preview.appendChild(h4);
      if (files) {
        [].forEach.call(files, readAndPreview);
      }
      function readAndPreview(file) {
        // Make sure `file` is an image
        if (/\.(jpe?g|png|gif)$/i.test(file.name)) {
          var reader = new FileReader();
          reader.addEventListener('load', function () {
            var image = new Image();
            image.title = file.name;
            image.src = this.result;
            preview.appendChild(image);
          });
          reader.readAsDataURL(file);
        }
      }
    }

    // Trigger image preview on file selection
    document.querySelector('input[type=file]').addEventListener('change', previewImages);
    document.getElementById('range').addEventListener('input', previewRange);
    // Prevent form submission if total file size exceeds 50MB
    document.querySelector('form').addEventListener('submit', function (e) {
      var files = document.querySelector('input[type=file]').files;
      var totalSize = 0;
      if (files && files.length > 5) {
        alert('You can only upload a maximum of 5 images.');
        return;
      }
      for (var i = 0; i < files.length; i++) {
        totalSize += files[i].size;
      }
      if (totalSize > 50 * 1024 * 1024) {
        e.preventDefault();
        alert("Total size of images should be less than 50MB.");
      }
      
    });