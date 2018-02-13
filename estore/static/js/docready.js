$(document).ready(function () {
    $check = $('.dropify').prev().hide()
    $('.dropify').dropify({
        messages: {
            'default': '在此处拖放文件或单击',
            'replace': '拖放或单击以替换',
            'remove': '移除',
            'error': '糟糕，发生了一些错误。'
        },
        error: {
            'fileSize': '文件太大（最大 {{ value }}）。',
            'minWidth': '图像宽度太小（最小{{ value }}px)。',
            'maxWidth': '图像宽度太大（最大{{ value }}px)。',
            'minHeight': '图像高度太小（最小{{ value }}px)。',
            'maxHeight': '图像宽度太大（最大{{ value }}px)。',
            'imageFormat': '图像格式不支持 (仅限 {{ value }})。',
            'fileExtension': '不支持的文件扩展名（仅限{{ value }}）。'
        }
    }).on('dropify.afterClear', function (/*event, element*/) {
        $check.attr('checked', true);
    }).on('dropify.fileReady', function (/*event, element*/) {
        $check.attr('checked', false);
    });
});