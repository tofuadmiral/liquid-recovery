"""Two page product pitch. One page for the wedge, one for the business."""
from pathlib import Path
import re
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether
from pypdf import PdfReader
R=Path(__file__).resolve().parent
INK=colors.HexColor('#1b3028');GREEN=colors.HexColor('#356b46');MUTED=colors.HexColor('#667160')
styles={
 'eyebrow':ParagraphStyle('eyebrow',fontName='Helvetica-Bold',fontSize=8,leading=10,textColor=GREEN,spaceAfter=15),
 'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=28,leading=31,textColor=INK,spaceAfter=14),
 'lead':ParagraphStyle('lead',fontName='Helvetica',fontSize=11.2,leading=15.4,textColor=INK,spaceAfter=15),
 'section':ParagraphStyle('section',fontName='Helvetica-Bold',fontSize=10.5,leading=13,textColor=GREEN,spaceBefore=10,spaceAfter=6),
 'bullet':ParagraphStyle('bullet',fontName='Helvetica',fontSize=10.3,leading=14.1,textColor=INK,leftIndent=12,firstLineIndent=-10,spaceAfter=6),
 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=7.4,leading=10,textColor=MUTED,spaceBefore=10),
}
pages=[[],[]]
def add(page,kind,text):
 visible=re.sub('<[^>]*>','',text)
 assert not any(c in visible for c in ['—','–','-','(',')']),visible
 pages[page].append((kind,text))
add(0,'eyebrow','RECOVERY  /  A PRODUCT BET FOR LIQUID AI  /  FUAD ALI')
add(0,'title','Give every machine<br/>a clearer next step.')
add(0,'lead','I would build Recovery, a local assistant that helps operators work through recurring packaging stops using the machine maker’s own procedures. Sell it to the OEM as a service capability it can ship across its installed base.')
add(0,'section','Start where support work repeats')
add(0,'bullet','<b>The moment:</b> an operator changes a case packer to a new product. It keeps stopping. The screen repeats an alarm, while the service specialist has to reconstruct the history and ask which checks already failed.')
add(0,'bullet','<b>The first customer:</b> an OEM carrying substantial included or warranty support. Its service leader buys; controls engineering helps deploy. Start with one nonrobotic side load case packer family and two recurring stop types. Qualify for a repeated machine design, an accountable procedure owner and an existing service budget.')
add(0,'section','Make the next step easier to trust')
add(0,'bullet','<b>Read the whole incident.</b> Bring together recent machine events, the operator’s observations and attempted checks. Find the procedure for that machine and software version.')
add(0,'bullet','<b>Give one useful response.</b> Show the original instruction, ask for missing evidence, or escalate with the history attached. Stop sending people through checks they have already tried.')
add(0,'bullet','<b>Keep the operator in control.</b> No automatic resets, parameter changes or invented repairs. Record what the person tried and whether the stop returned.')
add(0,'section','Why Liquid belongs in the product')
add(0,'bullet','<b>Use the model where language varies.</b> LFM2.5 with 2.6B parameters would turn operator notes into observations the approved workflow can use. Rules choose the response. The pilot must show that handling varied language costs less to maintain than forms and phrase rules.')
add(0,'bullet','<b>Useful at the machine.</b> Local inference can keep the workflow available without an external connection. Start on an existing industrial PC only if measured spare capacity allows it. Compare the cost with a plant server and cloud before choosing hardware.')
add(0,'section','The larger opportunity')
add(0,'bullet','<b>Turn service knowledge into a maintained product.</b> An OEM could give every customer a consistent recovery experience and reserve specialists for harder cases. Expand into adjacent packaging equipment after the first family works and a second OEM can deploy it economically.')
add(0,'small','Evidence gate: the replay changed the design. The model interprets notes; rules select the response. Full results retain the failures. Consistent interpretation on real incidents, hardware fit and customer savings remain unproved. <link href="https://github.com/tofuadmiral/liquid-recovery" color="#356b46">Inspect the replay and results</link>. Model fit: <link href="https://huggingface.co/LiquidAI/LFM2.5-2.6B" color="#356b46">Liquid model card</link>.')
add(1,'eyebrow','THE BUSINESS  /  FROM ONE MACHINE FAMILY TO A REPEATABLE PRODUCT')
add(1,'title','Sell through the OEM.<br/>Earn the renewal.')
add(1,'lead','The OEM already owns the machine relationship, service channel and procedures. Recovery gives it a capability to bundle into service contracts. Our business works when each deployment adds less work than the value it creates.')
add(1,'section','Charge for a result the buyer can capture')
add(1,'bullet','<b>Test the price:</b> $20K for an eight week pilot, credited against year one. Production starts at $30K per OEM each year plus $300 per enabled machine. Scope new machine families separately.')
add(1,'bullet','<b>Require a buyer return:</b> at 200 machines, the annual price is $90K. Target at least $180K in annual value after deployment and upkeep, through support capacity, avoided OEM travel or service margin. Four calls per machine, 20 minutes saved and $100 per hour yield only $26.7K. That account fails qualification.')
add(1,'section','Win the first ten users, then the next OEM')
add(1,'bullet','<b>Reach service leaders at Douglas and Massman</b> through industry introductions and PMMI contacts. Ask each for 20 recent support cases and access to two customer plants. Recruit ten users across service, controls, maintenance and operating shifts. These are research targets; no demand is validated.')
add(1,'bullet','<b>Prove repetition early.</b> Keep the app, validation and updates common; configure machine data and procedures. The OEM approves procedures; we own releases. A second machine needs configuration only. Target ten engineering days for a second OEM after access, counting OEM preparation too. Customer knowledge stays isolated.')
add(1,'section','Build an advantage that survives a better model')
add(1,'bullet','<b>Win on deployment and upkeep.</b> SOMIC, Pearson, Beckhoff and ei³ already offer relevant diagnostics or assistance. Test whether Recovery can deliver a bounded workflow with less integration work. Validated mappings, procedure compatibility and dependable updates must drive renewal.')
add(1,'bullet','<b>Size the path honestly.</b> Ten OEMs with 200 machines each imply $900K ARR. Fifty with 500 machines imply $9M. These are pricing scenarios, with expansion assumed. The eligible account count still needs research.')
add(1,'section','Make an eight week investment decision')
add(1,'bullet','<b>Run a gated pilot.</b> Two engineers own integration and workflow; I own discovery, labels and economics. Qualify in weeks one and two, integrate in three and four, shadow in five and six, then test supervised use and replication. Target 25% fewer specialist minutes per eligible incident.')
add(1,'bullet','<b>Stop when the case fails.</b> No usable history or procedure owner by week two; persistent unsupported selections; rules with lower upkeep; weak savings; costly hardware or onboarding; or buyers who reject production pricing after seeing value.')
add(1,'small','Sources: <link href="https://www.douglas-machine.com/products-solutions/case-and-tray-packers/" color="#356b46">Douglas</link>, <link href="https://massmanautomation.com/applications/cans-bottles/" color="#356b46">Massman</link>, <link href="https://us.somic-packaging.com/service/digital-services/" color="#356b46">SOMIC</link>, <link href="https://pearsonpkg.com/technical-service/remote-service-support/" color="#356b46">Pearson</link>, <link href="https://www.beckhoff.com/en-au/products/automation/twincat-projects-with-ai-supported-engineering/" color="#356b46">Beckhoff</link>, <link href="https://ei3.com/platform/iiot-feature/connected-ai" color="#356b46">ei³</link>. Availability differs by offering. AI assistance: Codex supported research, code, evaluation and writing under my direction. I will present the argument and its limits.')
story=[]
for i,page in enumerate(pages):
 for kind,text in page:
  if kind=='bullet':text='• '+text
  story.append(Paragraph(text,styles[kind]))
 if i==0:story.append(PageBreak())
def decorate(canvas,doc):
 canvas.setStrokeColor(colors.HexColor('#d7dfcf'));canvas.line(47,38,565,38)
 canvas.setFont('Helvetica',7);canvas.setFillColor(MUTED);canvas.drawString(47,26,'RECOVERY  /  FUAD ALI  /  NOVEMBER 2026');canvas.drawRightString(565,26,f'{doc.page} / 2')
out=R/'output/pdf/liquid-recovery-memo.pdf'
doc=SimpleDocTemplate(str(out),pagesize=(612,792),leftMargin=47,rightMargin=47,topMargin=38,bottomMargin=49,title='Recovery | Product pitch',author='Fuad Ali')
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
r=PdfReader(out);assert len(r.pages)==2,len(r.pages)
for i,p in enumerate(r.pages):
 text=p.extract_text();assert not any(c in text for c in ['—','–','-','(',')']);print('Page',i+1,'words',len(text.split()))
md=[]
for i,page in enumerate(pages):
 for kind,text in page:
  text=re.sub(r'<link href="([^"]+)" color="[^"]+">([^<]+)</link>',r'[\2](\1)',text).replace('<b>','**').replace('</b>','**').replace('<br/>',' ')
  md.append(('## ' if kind=='title' else '### ' if kind=='section' else '* ' if kind=='bullet' else '')+text+'\n')
 if not i:md.append('<!-- page break -->\n')
(R/'output/memo.md').write_text('\n'.join(md))
(R/'site/memo.pdf').write_bytes(out.read_bytes())
print(out)
