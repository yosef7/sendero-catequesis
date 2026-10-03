const csrf = document.querySelector('meta[name="csrf-token"]').content;
export async function api(path, method = 'GET', body) {
  const response = await fetch(`/api${path}`, {method, headers: {'Content-Type': 'application/json', 'X-CSRF-Token': csrf}, ...(body !== undefined ? {body: JSON.stringify(body)} : {})});
  if (response.status === 401) {location.href = '/login'; throw new Error('Inicia sesión nuevamente.');}
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || 'No se pudo guardar. Inténtalo nuevamente.');
  return result;
}
export const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const formatDate = value => new Intl.DateTimeFormat('es-PA', {day:'numeric',month:'short',year:'numeric'}).format(new Date(`${value}T12:00:00`));
