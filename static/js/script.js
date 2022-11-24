// reformat the code below
const button1 = document.querySelector("#btn1");
const button2 = document.querySelector("#btn2");
const button3 = document.querySelector("#btn3");
const button4 = document.querySelector("#btn4");
const button5 = document.querySelector("#btn5");
const button6 = document.querySelector("#btn6");
const buttonNext = document.querySelector("#btnNext");
const buttonPrev = document.querySelector("#btnPrev");
const submitButton = document.querySelector("#submit");
var r = document.querySelector(":root");
color_dict = {
  primary: "#2f35fa",
  danger: "#f52003",
  success: "#08ae66",
  dark: "#000000",
};
const theme = button1.classList[1].split("-")[1];
r.style.setProperty("--range_slider", color_dict["dark"]);
r.style.getP;

const allRanges = document.querySelectorAll(".range-wrap");
allRanges.forEach((wrap) => {
  const range = wrap.querySelector(".form-range");
  const bubble = wrap.querySelector(".bubble");
  bubble.classList.add("bg-dark");
  range.addEventListener("input", () => {
    setBubble(range, bubble);
  });
  setBubble(range, bubble);
});
let positive_samples = [];
let negative_samples = [];
// Functions are hoisted in JavaScript unless the strict JavaScript is used. Thefore you can define functions you use in your code after the code that uses them.
function setBubble(range, bubble) {
  const val = range.value;
  const min = range.min ? range.min : 0;
  const max = range.max ? range.max : 100;
  const newVal = Number(((val - min) * 100) / (max - min));
  bubble.innerHTML = val;
  // Sorta magic numbers based on size of the native UI thumb
  bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
  bubble.style.top = `1.3rem`;
}

// Carousel inner selection

const formList = document.querySelector(".carousel-inner");
const carouselItems = formList.querySelectorAll(".carousel-item");
// remove all carousel items active class and active class
const button_list = [button1, button2, button3, button4, button5, button6];
button1.addEventListener("click", () => {
  // First remove from others
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list.map((button) => button.classList.add("btn-outline-" + theme));
  // Add primary now
  button1.classList.add("btn-" + theme);
  button1.classList.remove("btn-outline-" + theme);
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  carouselItems[0].classList.add("active");
});
button2.addEventListener("click", (e) => {
  e.preventDefault();
  // First remove from others
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list.map((button) => button.classList.add("btn-outline-" + theme));
  // Add primary now
  button2.classList.add("btn-" + theme);
  button2.classList.remove("btn-outline-" + theme);
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  carouselItems[1].classList.add("active");
});
button3.addEventListener("click", (e) => {
  e.preventDefault();
  // First remove from others
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list.map((button) => button.classList.add("btn-outline-" + theme));
  // Add primary now
  button3.classList.add("btn-" + theme);
  button3.classList.remove("btn-outline-" + theme);
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  carouselItems[2].classList.add("active");
});
button4.addEventListener("click", (e) => {
  e.preventDefault();
  // First remove from others
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list.map((button) => button.classList.add("btn-outline-" + theme));
  // Add primary now
  button4.classList.add("btn-" + theme);
  button4.classList.remove("btn-outline-" + theme);
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  carouselItems[3].classList.add("active");
});
button5.addEventListener("click", (e) => {
  e.preventDefault();
  // First remove from others
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list.map((button) => button.classList.add("btn-outline-" + theme));
  // Add primary now
  button5.classList.add("btn-" + theme);
  button5.classList.remove("btn-outline-" + theme);
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  carouselItems[4].classList.add("active");
});
button6.addEventListener("click", (e) => {
  e.preventDefault();
  // First remove from others
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list.map((button) => button.classList.add("btn-outline-" + theme));
  // Add primary now
  button6.classList.add("btn-" + theme);
  button6.classList.remove("btn-outline-" + theme);
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  carouselItems[5].classList.add("active");
  submitButton.classList.remove("d-none");
});
buttonNext.addEventListener("click", (e) => {
  let active = document.querySelector(".carousel-item.active");
  // Get its ID
  e.preventDefault();
  let active_id = active.id;

  carouselItems.forEach((elem) => elem.classList.remove("active"));
  carouselItems[active_id - 1].classList.add("active");
  button_list.map((button) => button.classList.add("btn-outline-" + theme)); // add all btn-outline
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list[active_id].classList.remove("btn-outline-" + theme);
  button_list[active_id].classList.add("btn-" + theme);

  let next = active.nextElementSibling;
  if (next) {
    active.classList.remove("active");
    next.classList.add("active");
  }
  if (active_id == 5) {
    submitButton.classList.remove("d-none");
    return;
  }
});
buttonPrev.addEventListener("click", (e) => {
  e.preventDefault();
  let active = document.querySelector(".carousel-item.active");
  // Get its ID

  let active_id = active.id;
  if (active_id == 1) {
    return;
  }
  carouselItems.forEach((elem) => elem.classList.remove("active"));
  carouselItems[active_id - 2].classList.add("active");
  button_list.map((button) => button.classList.add("btn-outline-" + theme)); // add all btn-outline
  button_list.map((button) => button.classList.remove("btn-" + theme));
  button_list[active_id - 2].classList.remove("btn-outline-" + theme);
  button_list[active_id - 2].classList.add("btn-" + theme);
  let prev = active.previousElementSibling;
  if (prev) {
    active.classList.remove("active");
    prev.classList.add("active");
  }
});
// Draw polygons with the following code
// https://stackoverflow.com/questions/29441389/how-to-draw-polygon-on-canvas-with-mouse-clicks-pure-js
// JQuery Code
submitButton.addEventListener("click", (e) => {
  e.preventDefault();
  let fields = $(":input").serializeArray();
  fields.positive_samples = positive_samples;
  fields.negative_samples = negative_samples;
  console.log(fields);
  $.post("/postmethod", {
    jsdata: JSON.stringify(fields),
    negative_samples: JSON.stringify(negative_samples),
    positive_samples: JSON.stringify(positive_samples),
  });
});
var canvas = document.getElementById("canvas");
let context = canvas.getContext("2d");
context.strokeStyle = "#FF0000";
var cw = canvas.width;
var ch = canvas.height;
function reOffset() {
  var BB = canvas.getBoundingClientRect();
  offsetX = BB.left;

  offsetY = BB.top;
}
var offsetX, offsetY;
reOffset();
window.onscroll = function (e) {
  reOffset();
};

context.lineWidth = 2;
context.strokeStyle = "blue";

let coordinates = [];

$("#positives").click(function (e) {
  e.preventDefault();
  positive_samples.push(coordinates);
  coordinates = [];
  context.clearRect(0, 0, cw, ch);
});
$("#negatives").click(function (e) {
  e.preventDefault();
  negative_samples.push(coordinates);
  console.log(negative_samples);
  coordinates = [];
  context.clearRect(0, 0, cw, ch);
});
$("#clear").click(function (e) {
  e.preventDefault();
  coordinates = [];
  context.clearRect(0, 0, cw, ch);
});

$("#canvas").mousedown(function (e) {
  handleMouseDown(e);
});

function handleMouseDown(e) {
  // tell the browser we're handling this event
  e.preventDefault();
  e.stopPropagation();

  mouseX = parseInt(e.clientX - offsetX);
  mouseY = parseInt(e.clientY - offsetY);
  coordinates.push({ x: mouseX, y: mouseY });
  drawPolygon();
}

function drawPolygon() {
  context.clearRect(0, 0, cw, ch);
  context.beginPath();
  context.moveTo(coordinates[0].x, coordinates[0].y);
  for (index = 1; index < coordinates.length; index++) {
    context.lineTo(coordinates[index].x, coordinates[index].y);
  }
  context.strokeStyle = "blue";
  context.closePath();
  context.stroke();
}
// get values from array
