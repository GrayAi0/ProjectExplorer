var root = undefined


function getUrlParameter(name) {
  name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
  var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
  var results = regex.exec(location.search);
  return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
};

const project_name = getUrlParameter('pname')

$(document).ready(async () => {
const root = new Vue({
    el:".root",
    data: {
        theme: (await eel.IsDarkMode()()) ? 'dark' : 'light',
        files: await eel.GetAllScriptsFromProject(project_name)(),
        currentfile:0
    },
    methods: {
      selectFile: (file) => {
        root.currentfile = file.index
        code.innerHTML = hljs.highlight(hljs.getLanguage(file.lang) !== undefined ? file.lang : 'text', file.text).value || ' '
      },
      savefile: (file) => {

      },
    }

})


let temp = setInterval(() => {
    if(document.body) {
      document.body.setAttribute('class', `body-${root._data.theme}`)
      clearInterval(temp)
    }
}, 1);


///////////////////////////////////////////////
let firsrt = true
const code = document.querySelector('#code')
const misbehave = new Misbehave(code, {
  oninput : function() {
    code.innerHTML = hljs.highlight('python', code.innerText).value || ' '
    if(firsrt) {
      firsrt = false 
      return 
    }
    root.files[root.currentfile].text = code.innerText
  }
})

const pre = document.querySelector('#pre') 
pre.onclick = function() { 
  code.focus() 
  return false 
}
document_loadd() // save call of document_loadd - function

})





