"""Recorrido real en Chromium. Requiere playwright y una demo VACÍA en :5083 con --test-code.
Ejecutar: python3 scripts/verify_browser.py (instalar playwright en este intérprete).
Guarda imágenes y video ficticios en demo/ y artifacts/v1/.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/v1';out.mkdir(parents=True,exist_ok=True)
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context(viewport={'width':1280,'height':800},record_video_dir=str(out),record_video_size={'width':1280,'height':800})
    page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto('http://127.0.0.1:5083');page.locator('input[name=code]').fill('demo-ficticia');page.get_by_role('button',name='Entrar',exact=False).click()
    page.locator('#nav-groups').click();page.get_by_role('button',name='Crear período',exact=True).click()
    page.locator('[name=name]').fill('Formación 2026 · Ejemplo');page.locator('[name=starts]').fill('2026-01-01');page.locator('[name=ends]').fill('2026-12-31');page.locator('[type=submit]').click();page.wait_for_timeout(1500)
    page.get_by_role('button',name='Añadir grupo').click();page.locator('[name=name]').fill('Sábados · Grupo ficticio');page.locator('[type=submit]').click();page.wait_for_timeout(1500)
    page.wait_for_timeout(4000)
    page.screenshot(path=str(root/'demo/grupos.png'),full_page=True)
    page.locator('#nav-children').click();page.locator('#new-child').click();page.locator('[name=name]').fill('Valentina Ejemplo');page.locator('[name=group_id]').select_option(index=1)
    page.locator('[name=guardian_0]').fill('Ana Ejemplo');page.locator('[name=relationship_0]').fill('Madre');page.locator('[name=contact_0]').fill('555-0100')
    page.locator('summary',has_text='Responsable 2').click();page.locator('[name=guardian_1]').fill('Luis Ejemplo');page.locator('[name=relationship_1]').fill('Padre');page.locator('[name=contact_1]').fill('555-0101');page.locator('[type=submit]').click()
    page.get_by_role('heading',name='Valentina Ejemplo',exact=True).wait_for();page.wait_for_timeout(1500)
    page.locator('#attendance').click();page.locator('[name=topic]').fill('La acogida y la comunidad · ejemplo');page.locator('[name=enrollment_id]').select_option(index=1);page.locator('[type=submit]').click();page.wait_for_timeout(1500)
    page.locator('#note').click();page.locator('[name=note]').fill('Observación ficticia para revisar en el próximo encuentro.');page.locator('[type=submit]').click();page.wait_for_timeout(1500)
    page.locator('#generate-plan').click();start=time.monotonic();page.locator('#review-plan').wait_for(timeout=150000);duration=time.monotonic()-start
    page.locator('#review-plan').click();page.get_by_text('✓ Revisada por Noris',exact=False).wait_for();page.wait_for_timeout(1500)
    page.wait_for_timeout(4000)
    page.screenshot(path=str(root/'demo/ai-plan.png'),full_page=True)
    page.reload();page.get_by_role('heading',name='Un camino que crece contigo.').wait_for();page.locator('[data-child]').click();page.get_by_text('Ana Ejemplo · Madre',exact=False).wait_for();page.get_by_text('Luis Ejemplo · Padre',exact=False).wait_for()
    assert page.get_by_text('La acogida y la comunidad · ejemplo',exact=False).count()>0
    assert page.get_by_text('Revisión IA',exact=True).count()==1
    page.screenshot(path=str(root/'demo/recorrido.png'),full_page=True)
    # Check dialogs, all three views and actual mobile edits at two narrow widths.
    context2=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    context2.add_cookies(context.cookies());mobile=context2.new_page();mobile.on('pageerror',lambda error:errors.append(str(error)));mobile.goto('http://127.0.0.1:5083');mobile.locator('[data-child]').click();mobile.locator('#edit').click()
    mobile.locator('[name=contact_0]').fill('555-0199');mobile.locator('[type=submit]').click();mobile.get_by_text('555-0199',exact=False).wait_for();mobile.wait_for_timeout(5200);mobile.screenshot(path=str(root/'demo/movil.png'),full_page=True)
    checks=[]
    for width in (390,320):
        mobile.set_viewport_size({'width':width,'height':844})
        for view in ('detail','groups','settings','children'):
            if view!='detail':mobile.locator('#nav-'+view).click()
            else:
                mobile.locator('#nav-children').click();mobile.locator('[data-child]').click()
            mobile.wait_for_timeout(150)
            overflow=mobile.evaluate('document.documentElement.scrollWidth > innerWidth')
            checks.append({'width':width,'view':view,'horizontal_overflow':overflow});assert not overflow,(width,view)
    page.locator('#nav-groups').click();page.wait_for_timeout(300);page.screenshot(path=str(root/'demo/grupos.png'),full_page=True)
    page.locator('#nav-children').click();page.wait_for_timeout(300);page.screenshot(path=str(root/'demo/registro.png'),full_page=True)
    state=page.evaluate("fetch('/api/state').then(r=>r.json())")
    assert len(state['children'][0]['guardians'])==2 and state['children'][0]['guardians'][0]['contact']=='555-0199'
    assert state['children'][0]['plans'][0]['reviewed_at']
    result={'javascript_errors':errors,'viewport_checks':checks,'real_ollama_seconds':round(duration,2),'model':state['children'][0]['plans'][0]['model'],'workflow':'login → período → grupo → participante y dos responsables → asistencia y tema → observación → IA → revisión → recarga → edición móvil','fictional_data':True}
    (out/'browser-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    assert not errors,errors
    video=page.video;context2.close();context.close();video.save_as(str(out/'workflow.webm'));browser.close();print(json.dumps(result,ensure_ascii=False))
