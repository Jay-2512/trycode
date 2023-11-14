console.log("Rich text loaded")

var outputWindow =document.querySelector(".result-container")

var editor = ace.edit("editor");
editor.setTheme("ace/theme/twilight");
editor.session.setMode("ace/mode/c_cpp");

const getText = () => {
  outputWindow.innerHTML = editor.getValue();
}