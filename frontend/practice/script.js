getText("text_file.txt");
async function getText(file){
    let myobject = await fetch(file);
    let mytext = await myobject.text();
    document.getElementById("API_one").innerHTML=mytext;
}

const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
canvas.addEventListener("mousemove", function(event){
const x = event.clientX;
const y = event.clientY;
ctx.beginPath();
ctx.moveTo(x,y);
ctx.lineTo(x+1,y+1);
ctx.fillStyle = "green";
ctx.stroke()});
