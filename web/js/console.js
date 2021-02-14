var root = undefined

function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
};

const cid = getUrlParameter('cid')

async function run() {
    await eel.ExecuteConsole(cid)()
    root._data.is_started = await eel.GetConsoleStatus(cid)()
}

async function stop() {
    await eel.StopConsole(cid)()
    root._data.is_started = await eel.GetConsoleStatus(cid)()
}


$(document).ready(async function() {
window.onbeforeunload = closingCode;
function closingCode(){
    eel.DestroyConsole(cid)
}
watch_console_event()

root = new Vue({
    el:'.root',
    data: {
        is_started:await eel.GetConsoleStatus(cid)(),
        theme: (await eel.IsDarkMode()()) ? 'dark' : 'light'
    }
})

document.body.setAttribute('class', `body-${root._data.theme}`)

function initoutput(output) {
    let span = document.querySelector("body > div > div.conosle > span")
    html = ''

    for(let letter of output.split('')) {
     if (letter == '\n') {
         html += '<br>'
     }else if(letter == '\t') {
        html += '&nbsp;&nbsp;&nbsp;&nbsp;'
     }else {
         html += letter
     }
    }
    span.innerHTML = html

}

function watch_console_event() {
    let console_event = setInterval(async () => {
        let outputinfo = await eel.GetOutput(cid)()
        if(outputinfo == null) {
            clearInterval(console_event)
            for(element of document.getElementsByClassName('consolemanage')) {
                element.disabled = true
            }
            let span = document.querySelector("body > div > div.conosle > span")
            span.innerText = "this console is not exists"
            span.setAttribute('class', 'dis')
            doc_console.setAttribute('class', 'dis conosle')

            return
        }
        let ischanged = outputinfo[0], output = outputinfo[1]
        if (ischanged) {
            initoutput(output)
        }
    }, 100);

    // setInterval(async function () {
    //         try {
    //             let event = JSON.parse(
    //                 await eel.GetConsoleStatus(cid)()
    //             );

    //             if (event.type == 'output') {
    //                 initoutput(event.value);

    //             } else if (event.type == 'status') {
    //                 root._data.is_started = event.value;

    //             } else if (event.type == 'time') {
    //                 settime(event.value);
    //             }

    //         }
    //         catch { }

    //     }, 10)
}

var scroolInternal = undefined
var $console = $('.conosle')
var doc_console = document.getElementsByClassName('conosle')[0] 
$console.on('scroll', e => {
    let h = doc_console.scrollHeight - doc_console.scrollTop; 
    if(h < 800) {
        if (scroolInternal == undefined) {
            scroolInernal = setInterval(() => {
                let h = doc_console.scrollHeight - doc_console.scrollTop; 
                if(h < 800) {
                    doc_console.scrollTop = doc_console.scrollHeight;  
                }else {
                    clearInterval(scroolInternal)
                    scroolInternal = undefined            
                }
            }, 1)
        }
    }else {
        clearInterval(scroolInternal)
        scroolInternal = undefined
    }

})
let outputinfo = await eel.GetOutput(cid)(),
ischanged = outputinfo[0], output = outputinfo[1]

if (!(output == '')) {

    let span = document.querySelector("body > div > div.conosle > span")
    span.innerText = 'You need to run the conosle to see the output'
}else {
    initoutput(output)
}

document_loadd() // save call of document_loadd - function

})