(() => {
'use strict';
const body=document.body;
if(!body.classList.contains('blog108'))return;
const event=(name,extra={})=>{if(typeof window.gtag==='function')window.gtag('event',name,{page_language:body.dataset.language,product_group:body.dataset.group,...extra});};
document.querySelectorAll('article pre').forEach((pre,index)=>{
 const bar=document.createElement('div');bar.className='b108-copy';
 const btn=document.createElement('button');btn.type='button';btn.textContent=body.dataset.copy;
 const status=document.createElement('span');status.setAttribute('role','status');status.setAttribute('aria-live','polite');
 bar.append(btn,status);pre.before(bar);
 btn.addEventListener('click',async()=>{
  const value=pre.textContent;
  try{
   if(navigator.clipboard&&window.isSecureContext)await navigator.clipboard.writeText(value);
   else{const el=document.createElement('textarea');el.value=value;el.style.position='fixed';el.style.opacity='0';document.body.append(el);el.select();const ok=document.execCommand('copy');el.remove();if(!ok)throw new Error('copy');}
   status.textContent=body.dataset.copied;event('blog_prompt_copy',{prompt_index:index+1});
  }catch(err){status.textContent=body.dataset.failed;}
 });
});
document.querySelectorAll('.b108-demo').forEach(demo=>{
 const inputs=[...demo.querySelectorAll('input[type=checkbox]')];
 const update=()=>{demo.querySelector('output').textContent=inputs.map(i=>i.dataset.name+': '+(i.checked?demo.dataset.on:demo.dataset.off)).join(' / ');};
 inputs.forEach(i=>i.addEventListener('change',update));
 demo.querySelector('.b108-reset').addEventListener('click',()=>{inputs.forEach(i=>i.checked=true);update();});update();
});
document.querySelectorAll('a[data-blog-product]').forEach(a=>a.addEventListener('click',()=>event('blog_product_click',{destination_path:new URL(a.href,location.href).pathname})));
})();
