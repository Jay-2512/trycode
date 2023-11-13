window.onload =  () => {
    document.getElementById('code').addEventListener('change', setCodeName);
    document.getElementById('testcase').addEventListener('change', setTestName);
}


const setCodeName = (event)=> {
    var codeLabel = document.getElementById('code-label');
    const files = event.target.files;
    const fileName = files[0].name;
    codeLabel.innerText = fileName;
}

const setTestName = (event) =>{
    var testLabel = document.getElementById('testcase-label');
    const files = event.target.files;
    const fileName = files[0].name;
    testLabel.innerText = fileName;
}