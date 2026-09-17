/* No article text or clipboard contents are sent to analytics. */
(() => {
  'use strict';
  const article=document.querySelector('body.editorial-20260917 article#article');
  if(!article) return;
  const lang=(document.documentElement.lang||'en').toLowerCase();
  const words={ja:['コピー','コピーしました','コピーできませんでした。本文を選択してコピーしてください。'],en:['Copy','Copied','Copy failed. Select and copy the text.'],de:['Kopieren','Kopiert','Bitte den Text markieren und kopieren.'],fr:['Copier','Copié','Sélectionnez le texte pour le copier.'],es:['Copiar','Copiado','Selecciona el texto para copiarlo.'],it:['Copia','Copiato','Seleziona il testo per copiarlo.'],ko:['복사','복사했습니다','본문을 선택하여 복사해 주세요.'],'pt-br':['Copiar','Copiado','Selecione o texto para copiar.'],'zh-cn':['复制','已复制','请选择正文并复制。'],'zh-tw':['複製','已複製','請選取內文後複製。']}[lang]||['Copy','Copied','Select and copy the text.'];
  const articleId=article.dataset.articleId||location.pathname;
  const track=(event,data)=>{if(typeof window.gtag==='function') window.gtag('event',event,{article_id:articleId,page_language:lang,...data});};
  article.querySelectorAll('pre').forEach((pre,i)=>{
    const row=document.createElement('div');row.className='copy-row';
    const button=document.createElement('button');button.type='button';button.textContent=words[0];
    const status=document.createElement('span');status.className='copy-status';status.setAttribute('role','status');status.setAttribute('aria-live','polite');
    pre.id=pre.id||`copy-block-${i+1}`;button.setAttribute('aria-controls',pre.id);
    row.append(button,status);pre.before(row);
    button.addEventListener('click',async()=>{
      const text=pre.innerText;
      try{
        if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(text);}
        else{
          const area=document.createElement('textarea');area.value=text;area.setAttribute('readonly','');area.style.position='fixed';area.style.opacity='0';document.body.append(area);area.select();
          let ok=false;try{ok=document.execCommand('copy');}finally{area.remove();button.focus();}
          if(!ok)throw new Error('copy');
        }
        status.textContent=words[1];track('blog_copy',{block_id:pre.id});
      }catch(_){status.textContent=words[2];}
    });
  });
  article.addEventListener('click',(event)=>{
    const link=event.target.closest('a[href]');if(!link)return;
    const dest=new URL(link.href,location.href);
    if(dest.hostname==='lp.toybird.com'&&/^\/(?:en\/)?(?:prompt-ready|pocket-screen|pointer-cue|ai-memorize-sheet)\/$/.test(dest.pathname))track('blog_product_click',{product_path:dest.pathname});
  });
})();
