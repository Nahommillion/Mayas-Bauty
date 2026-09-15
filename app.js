const d=document.getElementById("date"); if(d)d.min=new Date().toISOString().slice(0,10);

function pick(name){
  const select=document.getElementById("service");
  [...select.options].forEach(o=>{if(o.textContent.toLowerCase().includes(name.toLowerCase())) select.value=o.value});
  document.getElementById("booking").scrollIntoView({behavior:"smooth"});
}
function submitBooking(e){
  e.preventDefault();
  document.getElementById("bookingMsg").textContent="✨ Appointment request received. Online confirmation will be connected when the booking backend is added.";
}
function filterGallery(cat,btn){
  document.querySelectorAll(".gallery-filters button").forEach(x=>x.classList.remove("selected"));btn.classList.add("selected");
  document.querySelectorAll(".gallery-item").forEach(x=>x.style.display=(cat==="all"||x.classList.contains(cat))?"block":"none");
}
function servicePhotos(e,id){
  const box=document.getElementById(id);
  [...e.target.files].forEach(file=>{
    const r=new FileReader();r.onload=()=>{const im=document.createElement("img");im.src=r.result;box.appendChild(im)};
    r.readAsDataURL(file);
  }); e.target.value="";
}
function galleryPhotos(e){
  const grid=document.getElementById("galleryGrid");
  [...e.target.files].forEach(file=>{
    const r=new FileReader();r.onload=()=>{const div=document.createElement("div");div.className="gallery-item owner-photo";div.innerHTML=`<img src="${r.result}"><span>✨ MAYA • Owner Photo</span>`;grid.appendChild(div)};
    r.readAsDataURL(file);
  }); e.target.value="";
}
const io=new IntersectionObserver(entries=>entries.forEach(en=>{if(en.isIntersecting){en.target.classList.add("show");io.unobserve(en.target)}}),{threshold:.12});
document.querySelectorAll(".reveal").forEach(x=>io.observe(x));
