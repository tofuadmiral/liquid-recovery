const {chromium}=require('playwright-core');
const assert=require('node:assert/strict'),fs=require('node:fs/promises'),http=require('node:http'),path=require('node:path');
(async()=>{
 const root=process.cwd();await fs.mkdir(path.join(root,'tmp/ui'),{recursive:true});
 const server=http.createServer(async(req,res)=>{try{const url=new URL(req.url,'http://localhost');if(url.pathname==='/favicon.ico'){res.writeHead(204);res.end();return;}const file=url.pathname==='/memo.pdf'?'memo.pdf':url.pathname==='/'?'index.html':null;if(!file){res.writeHead(404);res.end();return}const body=await fs.readFile(path.join(root,'site',file));res.writeHead(200,{'Content-Type':file.endsWith('pdf')?'application/pdf':'text/html; charset=utf-8'});res.end(body);}catch{res.writeHead(500);res.end();}});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const base='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_EXECUTABLE||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.locator('#story-title').waitFor();
  assert.equal(await page.locator('#machine-checks').innerText(),'1');
  await page.screenshot({path:'tmp/ui/terminal-desktop.png',fullPage:true});
  await page.locator('#play-btn').click();await page.waitForFunction(()=>document.querySelector('#chapter-index').textContent.startsWith('02'),{},{timeout:7000});
  await page.locator('#play-btn').click();assert.equal(await page.locator('#play-btn').getAttribute('aria-pressed'),'false');
  await page.getByRole('button',{name:'Step 4: Next check',exact:true}).click();assert.match(await page.locator('#story-title').innerText(),/setup checklist/);
  await page.screenshot({path:'tmp/ui/terminal-check.png',fullPage:true});
  await page.locator('#story-next').click();assert.equal(await page.locator('#machine-checks').innerText(),'2');
  await page.locator('#story-next').click();assert.match(await page.locator('#story-title').innerText(),/alarm details/);
  await page.locator('#story-source').click();assert.equal(await page.locator('#case-select').inputValue(),'F01b');
  await page.locator('#method-select').selectOption('decision_tree');assert.match(await page.locator('.next-card h2').innerText(),/alarm details/);
  await page.locator('a.ref').first().click();assert.equal(await page.locator('#evidence-details').evaluate(e=>e.open),true);
  await page.locator('#tab-evaluation').click();assert.match(await page.locator('#evaluation-body').innerText(),/24 invented incidents/);
  await page.screenshot({path:'tmp/ui/terminal-results.png',fullPage:true});
  assert.equal((await page.request.get(base+'/memo.pdf')).status(),200);
  for(const width of [390,768,1440]){
   await page.setViewportSize({width,height:900});await page.locator('#tab-story').click();
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`Horizontal overflow at ${width}`);
   if(width===390)await page.screenshot({path:'tmp/ui/terminal-mobile.png',fullPage:true});
  }
  await page.emulateMedia({reducedMotion:'reduce'});assert.equal(await page.locator('.parcel').first().evaluate(e=>getComputedStyle(e).animationName),'none');
  assert.deepEqual(errors,[]);
  const report={passed:true,checks:['Recorded story advances and pauses','Paired cases change the next step','Case and method navigation','Evidence links open records','Results visible','Memo reachable','No horizontal overflow at 390, 768 and 1440 pixels','Reduced motion respected','No browser script errors'],screenshots:['terminal-desktop.png','terminal-check.png','terminal-results.png','terminal-mobile.png']};
  await fs.writeFile('results/terminal-browser-tests.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
 }finally{await browser.close();await new Promise(resolve=>server.close(resolve))}
})().catch(e=>{console.error(e);process.exitCode=1});
