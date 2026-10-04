import {api, escape as e} from './api.js';

function planBody(plan) {
  const facts=plan.evidence;
  return `<div class="plan-facts"><span>${facts.asistencias} de ${facts.clases_registradas} asistencias registradas</span><span>${facts.requisitos.filter(r=>r.cumplido).length} de ${facts.requisitos.length} requisitos verificados</span></div><h3>Pendientes para revisar</h3><p>${plan.content.pending_numbers.length?'Requisitos: '+plan.content.pending_numbers.map(n=>e(n)).join(', '):'Sin requisitos pendientes en esta etapa.'}</p><h3>Preparar el próximo encuentro</h3><ol class="plan-steps">${plan.content.preparation.map(step=>`<li>${e(step)}</li>`).join('')}</ol><h3>Una pregunta para el responsable</h3><p>${e(plan.content.family_question)}</p><p class="muted"><small>Generado con ${e(plan.model)} · ${e(plan.created_at)} UTC</small></p>`;
}

export function renderPlan(child) {
  const latest=child.plans[0];
  return `<section class="panel ai-panel"><p class="eyebrow">ACOMPAÑAMIENTO CON IA ABIERTA</p><h2>Su próximo paso empieza aquí</h2><p>Prepara una propuesta de encuentro a partir de su progreso. La IA funciona en tu equipo.</p>${latest?.outdated?'<div class="notice">El registro cambió desde esta propuesta. Genera una nueva antes de preparar el encuentro.</div>':''}<button id="generate-plan" class="primary" ${child.archived?'disabled':''}>✧ ${latest?'Actualizar propuesta':'Preparar acompañamiento'}</button><p id="plan-status" role="status" class="muted"></p>${latest?`<div class="ai-output">${planBody(latest)}<p>${latest.reviewed_at?'✓ Revisada por el equipo de catequesis · '+e(latest.reviewed_at)+' UTC':'Propuesta pendiente de revisión'}</p><button id="review-plan" ${latest.outdated||latest.reviewed_at||child.archived?'disabled':''}>Marcar como revisada</button></div>`:'<p class="muted">Aquí aparecerán ideas para revisar los pendientes y conversar con el responsable.</p>'}<small>Son sugerencias para revisar, no hechos confirmados ni una autorización de avance. No se envían nombres, contactos, temas ni observaciones al modelo.</small>${child.plans.length>1?`<details class="plan-history"><summary>Propuestas anteriores (${child.plans.length-1})</summary>${child.plans.slice(1).map(p=>`<article class="old-plan">${planBody(p)}</article>`).join('')}</details>`:''}</section>`;
}

export function bindPlan(child,refresh) {
  const review=document.querySelector('#review-plan');
  if(review)review.onclick=async()=>{review.disabled=true;try{await api(`/children/${child.id}/plans/${child.plans[0].id}/review`,'POST',{});await refresh();}catch(err){document.querySelector('#plan-status').textContent=err.message;review.disabled=false;}};
  document.querySelector('#generate-plan').onclick=async event=>{
    const button=event.currentTarget, status=document.querySelector('#plan-status');
    button.disabled=true;status.textContent='Preparando el encuentro con la IA local…';
    try {await api(`/children/${child.id}/plan`,'POST',{});await refresh();}
    catch(error){status.textContent=error.message;button.disabled=false;}
  };
}
