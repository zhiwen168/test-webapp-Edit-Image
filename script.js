let fileId = new URLSearchParams(window.location.search).get('file_id');
let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
let cropBtn = document.getElementById('cropBtn');

if (fileId) {
    fetch(`https://api.telegram.org/bot7203250432:AAEHdEZHk4MXWnyFXkY_Soh-kDEcoOLncW0/getFile?file_id=${fileId}`)
        .then(response => response.json())
        .then(data => {
            if (data.ok) {
                let filePath = data.result.file_path;
                let imageUrl = `https://api.telegram.org/file/bot7203250432:AAEHdEZHk4MXWnyFXkY_Soh-kDEcoOLncW0/${filePath}`;

                let img = new Image();
                img.crossOrigin = "Anonymous";
                img.src = imageUrl;
                img.onload = function() {
                    canvas.width = img.width;
                    canvas.height = img.height;
                    ctx.drawImage(img, 0, 0, img.width, img.height);

                    // 启用裁剪按钮
                    cropBtn.disabled = false;
                };
            } else {
                alert('无法获取图片，请重试。');
            }
        })
        .catch(error => {
            console.error('获取图片失败:', error);
        });
} else {
    alert('未找到图片 ID。');
}

// 裁剪功能
cropBtn.addEventListener('click', function() {
    let cropWidth = 200;  // 裁剪宽度
    let cropHeight = 200; // 裁剪高度
    let x = (canvas.width - cropWidth) / 2; // 居中裁剪
    let y = (canvas.height - cropHeight) / 2;

    let croppedImageData = ctx.getImageData(x, y, cropWidth, cropHeight);
    
    let croppedCanvas = document.createElement('canvas');
    croppedCanvas.width = cropWidth;
    croppedCanvas.height = cropHeight;
    let croppedCtx = croppedCanvas.getContext('2d');
    croppedCtx.putImageData(croppedImageData, 0, 0);

    croppedCanvas.toBlob(blob => {
        let formData = new FormData();
        formData.append('photo', blob, 'cropped.jpg');

        // 发送到 Telegram 机器人
        fetch(`https://api.telegram.org/bot7203250432:AAEHdEZHk4MXWnyFXkY_Soh-kDEcoOLncW0/sendPhoto`, {
            method: 'POST',
            body: formData
        }).then(response => response.json())
          .then(data => {
              if (data.ok) {
                  alert('图片裁剪成功，已发送回 Telegram！');
              } else {
                  alert('图片发送失败，请重试。');
              }
          })
          .catch(error => {
              console.error('上传失败:', error);
          });
    }, 'image/jpeg');
});
