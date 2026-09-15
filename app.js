const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('show'); });
}, {threshold:.08});
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

const date = document.querySelector('input[type="date"]');
if (date) date.min = new Date().toISOString().slice(0,10);

function showBookingMessage(){
  const box=document.getElementById('booking-message');
  box.textContent='✨ Thank you! Your appointment request is ready. Telegram synchronization will be connected next.';
  box.scrollIntoView({behavior:'smooth',block:'center'});
}

document.querySelector('.menu-toggle')?.addEventListener('click',()=>{
  const nav=document.querySelector('.nav');
  const actions=document.querySelector('.header-actions');
  const open=nav.style.display==='flex';
  nav.style.display=open?'none':'flex';
  actions.style.display=open?'none':'flex';
  nav.style.position='absolute'; nav.style.top='76px'; nav.style.left='0'; nav.style.right='0';
  nav.style.background='#0b0907'; nav.style.padding='22px'; nav.style.flexDirection='column';
  actions.style.position='absolute'; actions.style.top='360px'; actions.style.left='0'; actions.style.right='0';
  actions.style.background='#0b0907'; actions.style.padding='20px'; actions.style.justifyContent='center';
});
