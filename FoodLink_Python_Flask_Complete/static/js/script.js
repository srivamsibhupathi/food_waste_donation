function toggleNav(){document.getElementById("nav").classList.toggle("open")}
setTimeout(()=>document.querySelectorAll(".toast").forEach(x=>x.remove()),5000);
document.querySelectorAll(".notify").forEach(x=>x.addEventListener("click",()=>x.classList.toggle("active")));
window.addEventListener("pageshow",function(){document.querySelectorAll("form.form-card input[type=number]").forEach(function(i){if(!i.value)i.value="";});});
