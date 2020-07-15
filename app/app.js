
function onCvLoaded() {
    console.log('cv', cv);
    cv.onRuntimeInitialized = testCSV;
}

const video = document.getElementById('video');

const actionBtn = document.getElementById('actionBtn');

const FPS = 30;
let stream;
let streaming = false;
let data;
let count = 0;

async function testCSV() {
    data = await d3.csv("../resources/3d-annotation.csv").then(function (res) {
        return res
    });
    setTimeout(onReady, 0);
}

function onReady() {
    console.log('ready');
    let src;
    let dst;
    let cap;

    video.controls = true;
    video.addEventListener('play', start);
    video.addEventListener('pause', stop);
    video.addEventListener('ended', stop);

    function start() {
        console.log('playing...');
        streaming = true;
        const width = video.width;
        const height = video.height;
        src = new cv.Mat(height, width, cv.CV_8UC4);
        dst = new cv.Mat(height, width, cv.CV_8UC1);
        cap = new cv.VideoCapture(video);
        console.log(data)
        setTimeout(processVideo, 0);
    }

    function stop() {
        console.log('paused or ended');
        streaming = false;
    }

    function drawFace(points) {
        let j;
        for(let i = 0; i < points.length; i++) {
            j = i + 1
            if(i + 1 == points.length) {
                j = 0
            }
            cv.line(dst, new cv.Point(parseInt(points[i][0]), parseInt(points[i][1])),
                new cv.Point(parseInt(points[j][0]), parseInt(points[j][1])), [0, 0, 255, 0], 2)
        }
    }

    function overlayOnImage(frameData) {
        if(frameData['points'] == '') {
            return
        }
        points = JSON.parse(frameData['points']);
        faces = JSON.parse(frameData['faces']);
        
        faces.forEach(face => {
            drawFace([points[face[0]], points[face[1]], points[face[2]], points[face[3]]])
        });
    }

    function processVideo() {
        if (!streaming) {
            src.delete();
            dst.delete();
            return;
        }
        const begin = Date.now();
        cap.read(src)

        // To rotate the image
        let dsize = new cv.Size(src.rows, src.cols);
        let center = new cv.Point(src.cols / 2, src.rows / 2);
        let M = cv.getRotationMatrix2D(center, 90, 1);
        cv.warpAffine(src, dst, M, dsize, cv.INTER_LINEAR, cv.BORDER_CONSTANT, new cv.Scalar());
        // to change colour
        cv.cvtColor(dst, dst, cv.COLOR_RGBA2RGB);

        overlayOnImage(data[count]);

        cv.imshow('canvasOutput', dst);

        const delay = 1000 / FPS - (Date.now() - begin);
        count++;
        setTimeout(processVideo, delay);
    }
}
