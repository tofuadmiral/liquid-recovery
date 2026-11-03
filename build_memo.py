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
add(0,'eyebrow','LIQUID AI  /  PRODUCT PROPOSAL  /  FUAD ALI')
add(0,'title','Recovery for<br/>packaging machines')
add(0,'lead','An operator switches products. The machine stops, they check the product settings, and it stops again with the same alarm. I would build Recovery to show the next useful check using the manufacturer’s instructions and what the operator already tried. The equipment maker’s service team would buy it.')
add(0,'section','The first customer and problem')
add(0,'bullet','Start with one family of case packing machines, without robots, and two common stops after a product change. The first user is an operator or maintenance technician who needs to know which check to try next and when to call service.')
add(0,'bullet','I would choose packaging before consumer assistants because we can look for a repeated machine design, someone responsible for the instructions, and a service team already spending money on the problem. I would target manufacturers that pay for substantial warranty or included support.')
add(0,'section','What the operator sees')
add(0,'bullet','Recovery shows one check from the manufacturer’s instructions and the events that explain why it applies. It remembers completed checks so the operator can move on to the next one.')
add(0,'bullet','If records disagree or information is missing, it asks for clarification. If the checks keep failing, it sends the history to a service specialist.')
add(0,'bullet','A person performs the check and confirms what happened. Recovery never resets the machine, changes settings or writes repair instructions.')
add(0,'section','Why use Liquid')
add(0,'bullet','I would start with LFM2.5 with 2.6B parameters to read operator notes. People describe the same problem in different ways. The model turns those notes into facts; ordinary software chooses the next approved check. If forms and simple rules do the job with less upkeep, we should use them.')
add(0,'bullet','Running on the machine’s existing computer could keep the assistant available without internet access. We would first check available memory and performance, then compare the cost with a shared factory server or cloud service.')
add(0,'section','The first eight weeks')
add(0,'bullet','Use the first two weeks to review support cases and agree on instructions. Connect the data in weeks three and four. Let service staff review recommendations in weeks five and six, then try supervised use on two machines. Two engineers build it; I lead customer research and measure the results.')
add(0,'bullet','The target is 25% less specialist time per relevant support case. We need to show that saving before expanding to more machines.')
add(0,'small','The demo uses invented incidents. The assistant and rules alone both passed 24 examples, so the test does not establish a need for the model. Customer savings and factory hardware performance still need testing. <link href="https://liquid-recovery.vercel.app/" color="#356b46">Demo and results</link> · <link href="https://huggingface.co/LiquidAI/LFM2.5-2.6B" color="#356b46">Liquid model card</link>.')
add(1,'eyebrow','RECOVERY  /  CUSTOMERS AND LONG TERM VALUE')
add(1,'title','Customers and<br/>long term value')
add(1,'lead','The service leader at an equipment manufacturer would buy Recovery from the service budget. This would be their first purchase from Liquid. They could include it in the support contracts they already sell to factories.')
add(1,'section','Finding customers and testing the price')
add(1,'bullet','Start with Douglas and Massman through industry introductions and PMMI, the packaging industry association. Ask each for 20 recent support cases and access to two customer plants. Recruit ten people across service, engineering, maintenance and operating shifts. These are prospects; I have not validated demand.')
add(1,'bullet','Test a $20K eight week pilot, credited against the first year. Then charge $30K per manufacturer each year plus $300 per machine. At 200 machines, that is $90K a year.')
add(1,'bullet','I would look for at least $180K in yearly value after setup and upkeep, from saved support time, avoided travel or added service profit. Four calls per machine, 20 minutes saved and $100 per hour produce only $26.7K. That customer would not justify the price.')
add(1,'section','How the value grows over time')
add(1,'bullet','Each machine builds a history of its software version, product settings, alarms, attempted checks and confirmed outcomes. Service engineers review recurring problems and improve the instructions and the examples used to interpret notes. The next operator starts with that knowledge.')
add(1,'bullet','Those past cases also become tests that every update must pass. Over time, replacing Recovery would mean rebuilding and checking that machine knowledge. Customers would own and be able to export their records. We would keep their service knowledge separate.')
add(1,'bullet','If models become interchangeable, customers would still pay for accurate machine connections, current instructions and updates they can trust. SOMIC, Pearson, Beckhoff and ei³ already offer relevant support tools. We have to show that ours takes less work to set up and maintain.')
add(1,'section','Growing beyond the first customer')
add(1,'bullet','Reuse the app, testing tools and update process. Change the machine connections and instructions for each manufacturer. A second machine should only need its data and instructions added. A second manufacturer must fit ten engineering days after access is ready, counting their preparation too. Expand to other equipment only after that works.')
add(1,'bullet','Ten manufacturers with 200 machines each would bring in $900K a year. Fifty with 500 machines would bring in $9M. These are scenarios based on the proposed price. I still need to establish how many buyers fit.')
add(1,'bullet','I would stop if we cannot get usable records or someone responsible for the instructions by week two, recommendations remain unreliable, support time does not fall, setup exceeds the time limit, hardware removes the savings, or buyers reject the price after seeing results.')
add(1,'small','Public sources: <link href="https://www.douglas-machine.com/products-solutions/case-and-tray-packers/" color="#356b46">Douglas</link>, <link href="https://massmanautomation.com/applications/cans-bottles/" color="#356b46">Massman</link>, <link href="https://us.somic-packaging.com/service/digital-services/" color="#356b46">SOMIC</link>, <link href="https://pearsonpkg.com/technical-service/remote-service-support/" color="#356b46">Pearson</link>, <link href="https://www.beckhoff.com/en-au/products/automation/twincat-projects-with-ai-supported-engineering/" color="#356b46">Beckhoff</link>, <link href="https://ei3.com/platform/iiot-feature/connected-ai" color="#356b46">ei³</link>. Capabilities vary by product. Codex helped with research, code, testing and writing under my direction.')
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
