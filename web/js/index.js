

var root = undefined
var languages = {}

$(document).ready(async () => {

languages = await eel.GetAvailableLanguages()()
console.log(languages)
root = new Vue({
    el:".root",
    data: {
        projects: await eel.GetProjects()(),
        theme: (await eel.IsDarkMode()()) ? 'dark' : 'light',
        langs: await eel.GetAvailableLanguages()(),
    },

    methods: {
      GetLanguage:function(lang_id) {
        return languages[lang_id] || {
          ext: '.unk',
          key: 'unknown',
          name: 'unknown lang',

        }
      }
    }

})

document_loadd() // save call of document_loadd - function
})


function DeleteProject(proj_name) {
  eel.DeleteProject(proj_name)().then(is_deleted => {
    if(is_deleted) {
      eel.GetProjects()().then(ps => root._data.projects = ps)
    }
  })
}

let temp = setInterval(() => {
  if(document.body && root) {
    document.body.setAttribute('class', `body-${root._data.theme}`)
    clearInterval(temp)
  }
}, 1);


function Accordion_clicked(elm) {
    /* Toggle between adding and removing the "active" class,
    to highlight the button that controls the panel */
    elm.classList.toggle("active");

    /* Toggle between hiding and showing the active panel */
    var panel = elm.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }


    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }

}

var current_lang = undefined

function lang_chose(btn) {
  current_lang = btn.getAttribute('lang-data')
  document.getElementById("chose_one").innerText = `You Chose: ${btn.innerText}`
}



async function CreateProject() {
  let name = document.getElementById('proj-name').value.replace(" ", '_')
  let desc = document.getElementById('proj-desc').value
  let lang = current_lang
  if (name == '' ) {
    return alert("Project name required")
  }
  if(current_lang == undefined) {
    return alert("Chose language first")
  }
  
  let is_created = await eel.CreateProject(name, desc, lang)()

  if(is_created) {
    root._data.projects = await await eel.GetProjects()()
    return alert(is_created)
  } 


}
consoleobj = undefined
async function run_project(proj_name) {
  let cid = await eel.CreateConsole(proj_name, false)()
  if(cid == false) {
    return alert("Failed to create the console")
  }
  consoleobj = await  eel.GetConsole(cid)()
  windw = window.open(`${window.location.origin}/console.html?cid=${cid}`);
}

async function quick_open(project) {
  window.open(`${window.location.origin}/edit.html?pname=${project}`);
}
