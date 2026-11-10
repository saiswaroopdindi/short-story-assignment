from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from pathlib import Path

OUT = Path('slides/autoencoder-deep-clustering.pdf')
W, H = landscape((1280, 720))
NAVY = colors.HexColor('#07152F')
INK = colors.HexColor('#10213F')
MUTED = colors.HexColor('#5274A8')
BLUE = colors.HexColor('#EAF3FF')
PURPLE = colors.HexColor('#EEE8FF')
GREEN = colors.HexColor('#E9FBF5')
ORANGE = colors.HexColor('#FFF5E8')

def wrap(text, font, size, max_width):
    words = text.split()
    lines, line = [], ''
    for word in words:
        candidate = (line + ' ' + word).strip()
        if stringWidth(candidate, font, size) <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def text(c, value, x, y, width, size=22, color=INK, bold=False, leading=None):
    font = 'Helvetica-Bold' if bold else 'Helvetica'
    leading = leading or size * 1.25
    c.setFillColor(color)
    c.setFont(font, size)
    yy = y
    for paragraph in value.split('\n'):
        for line in wrap(paragraph, font, size, width):
            c.drawString(x, yy, line)
            yy -= leading
        yy -= leading * .15
    return yy

def rect(c, x, y, w, h, fill, stroke=colors.HexColor('#D7E2F1')):
    c.setFillColor(fill); c.setStrokeColor(stroke); c.roundRect(x, y, w, h, 14, fill=1, stroke=1)

def slide_base(c, kicker, title):
    c.setFillColor(colors.HexColor('#F7FAFE')); c.rect(0, 0, W, H, fill=1, stroke=0)
    text(c, kicker.upper(), 64, H-62, 900, 13, MUTED, True)
    text(c, title, 64, H-110, 1120, 32, INK, True)

def cover(c):
    c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
    img = ImageReader('assets/autoencoder-clustering-hero.png')
    c.drawImage(img, 520, 0, width=760, height=720, preserveAspectRatio=True, mask='auto')
    text(c, 'CMPE 255  |  DATA MINING SURVEY', 72, 630, 430, 16, colors.HexColor('#6ED6FF'), True)
    text(c, 'Autoencoder-Based Deep Clustering', 72, 545, 470, 44, colors.white, True, 52)
    text(c, 'How representation learning turns high-dimensional data into clustering-friendly structure', 76, 340, 430, 21, colors.HexColor('#C8D6F2'), False, 27)
    text(c, 'Based on Leiber, Miklautz, Plant & Böhm (arXiv:2504.02087v2)', 76, 88, 450, 13, colors.HexColor('#91A8CE'))

def make_pdf():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(W,H))
    cover(c); c.showPage()

    slide_base(c, '01 | Why this topic', 'The data mining problem')
    text(c, 'Traditional clustering sees the raw feature space. Deep clustering learns a space where the grouping task becomes easier.', 72, 548, 1120, 24, colors.HexColor('#243B64'))
    for x, fill, head, body, col in [(76,BLUE,'High-dimensional input','Images, text, tabular records',colors.HexColor('#0B4D8D')),(430,PURPLE,'Learned representation','A compact nonlinear embedding',colors.HexColor('#5635A4')),(815,GREEN,'Cluster structure','Compact groups and clearer boundaries',colors.HexColor('#08734D'))]:
        rect(c,x,270,300,180,fill); text(c,head,x+24,405,250,20,col,True); text(c,body,x+24,345,250,18,colors.HexColor('#2E5A86'))
    text(c, 'The survey treats autoencoders as a reusable sandbox: the encoder changes the geometry, while the clustering objective decides what “useful” means.', 76, 150, 1040, 21, colors.HexColor('#243B64'))
    c.showPage()

    slide_base(c, '02 | Survey map', 'One taxonomy, three training loops')
    text(c, 'The key distinction is how representation learning and clustering influence each other.', 72, 548, 1080, 22, colors.HexColor('#243B64'))
    data=[('Sequential','Train AE, then cluster embedding','Simple and modular. The embedding may ignore the task.',BLUE,colors.HexColor('#0B4D8D')),('Alternating','Update embedding and clusters in turn','Representation and labels refine each other.',ORANGE,colors.HexColor('#9A5A00')),('Simultaneous','Optimize reconstruction and clustering together','Joint objective with tighter coupling.',PURPLE,colors.HexColor('#5635A4'))]
    for i,(h,b,body,fill,col) in enumerate(data):
        x=76+i*382; rect(c,x,260,330,250,fill); text(c,h,x+24,450,280,24,col,True); text(c,b,x+24,385,280,19,INK,True); text(c,body,x+24,315,280,17,colors.HexColor('#5E7194'))
    text(c, 'Representative methods include AE + k-Means, N2D, DEC, IDEC, DCEC, DCN and DKM.', 76, 1120 if False else 104, 1060, 18, MUTED)
    c.showPage()

    slide_base(c, '03 | Architecture', 'The autoencoder is the representation engine')
    text(c, 'An encoder compresses x into z. A decoder reconstructs x from z. The bottleneck makes the latent space explicit.', 72, 548, 1090, 22, colors.HexColor('#243B64'))
    labels=['Input x','Encoder','Latent z','Decoder','Reconstruction x-hat']; fills=[BLUE,BLUE,PURPLE,BLUE,GREEN]
    for i,label in enumerate(labels):
        x=72+i*248; rect(c,x,300,160,110,fills[i]); text(c,label,x+14,355,135,18,INK,True)
        if i<4: text(c,'→',x+175,335,40,28,MUTED,True)
    text(c, 'A common fully connected backbone uses a mirrored encoder and decoder with a low-dimensional bottleneck. Convolutional variants fit image structure better.', 76, 180, 1040, 20, colors.HexColor('#243B64'))
    text(c, 'A low reconstruction error does not guarantee clusters that match the downstream task.', 76, 100, 1050, 19, colors.HexColor('#9A5A00'), True)
    c.showPage()

    slide_base(c, '04 | Objectives', 'Loss design controls the trade-off')
    text(c, 'Deep clustering methods add a clustering signal to reconstruction. The balance changes what the latent space preserves.', 72, 548, 1090, 22, colors.HexColor('#243B64'))
    rect(c,88,270,480,220,colors.white); text(c,'Reconstruction loss',120,440,380,23,colors.HexColor('#0B4D8D'),True); text(c,'Keeps decoded samples close to the input.\nUseful when preserving information matters.',120,365,360,19,INK)
    rect(c,712,270,480,220,colors.white); text(c,'Clustering loss',744,440,380,23,colors.HexColor('#5635A4'),True); text(c,'Pulls the embedding toward compact,\nseparable or task-specific groups.',744,365,380,19,INK)
    text(c, 'Total objective = reconstruction term + weighted clustering term', 160, 190, 960, 26, INK, True)
    text(c, 'The weight is a modeling decision, not a detail.', 160, 125, 960, 18, MUTED)
    c.showPage()

    slide_base(c, '05 | Method comparison', 'What the methods gain, and what they give up')
    rows=[('AE + k-Means','Easy baseline','No task feedback after embedding'),('N2D','Uses a learned manifold','New-sample prediction is awkward'),('DEC / IDEC','Shapes latent space','Sensitive to initialization and loss balance'),('DCEC','Convolutional bias','More tied to image-like inputs'),('DKM','Deep k-Means objective','Requires careful optimization choices')]
    for i,(a,b,d) in enumerate(rows):
        y=420-i*62; rect(c,72,y,1130,48,colors.white if i%2 else colors.HexColor('#F0F5FB')); text(c,a,90,y+30,250,17,INK,True); text(c,b,380,y+30,330,17,INK); text(c,d,760,y+30,400,17,colors.HexColor('#5E7194'))
    text(c, 'The strongest contribution is the shared design space. Many methods differ less in the encoder than in how clustering evidence feeds back into training.', 76, 74, 1080, 18, colors.HexColor('#0B4D8D'), True)
    c.showPage()

    slide_base(c, '06 | Evaluation', 'Metrics can reward different stories')
    text(c, 'A credible comparison needs more than one score. External labels, internal geometry and stability answer different questions.', 72, 548, 1120, 22, colors.HexColor('#243B64'))
    rows=[('External','ARI, NMI, ACC','Do groups align with known labels?'),('Internal','Silhouette, WCSS','Are points compact and separated?'),('Robustness','Seeds, perturbations','Does the solution survive randomness?'),('Practical','Inference, scalability','Can the model label new samples?')]
    for i,(a,b,d) in enumerate(rows):
        y=405-i*72; rect(c,80,y,1120,54,ORANGE if i==1 else colors.white); text(c,a,104,y+33,150,18,colors.HexColor('#5635A4'),True); text(c,b,300,y+33,290,18,INK,True); text(c,d,640,y+33,500,17,colors.HexColor('#5E7194'))
    text(c, 'Ablation question: how much of the gain comes from the autoencoder, clustering term, augmentation or optimizer?', 80, 90, 1100, 18, colors.HexColor('#9A5A00'), True)
    c.showPage()

    slide_base(c, '07 | Open questions', 'Where the survey points next')
    items=[('Representation quality','Separate semantic structure from nuisance variation?'),('Unknown cluster count','Decide k without labels?'),('Shift and deployment','Keep clusters meaningful as data moves?'),('Evaluation practice','Report stability and compute cost consistently?')]
    for i,(a,b) in enumerate(items):
        x=80+(i%2)*560; y=340-(i//2)*160; rect(c,x,y,500,118,PURPLE if i%2 else BLUE); text(c,a,x+24,y+78,440,20,colors.HexColor('#5635A4') if i%2 else colors.HexColor('#0B4D8D'),True); text(c,b,x+24,y+38,440,17,INK)
    text(c, 'The data mining lesson is broader than one algorithm: representation learning changes the space in which similarity is defined.', 80, 96, 1080, 21, INK, True)
    c.showPage()

    slide_base(c, '08 | Conclusion', 'Takeaways for a data mining practitioner')
    take=['Start with AE + k-Means as a transparent baseline','Add clustering feedback only when the baseline exposes a real failure','Report metrics, seeds, ablations and deployment behavior together','Treat the latent space as a modeling decision, not a visualization afterthought']
    for i,item in enumerate(take):
        y=470-i*82; text(c,str(i+1),90,y,60,28,colors.HexColor('#6B4FE6'),True); text(c,item,170,y-2,980,24,INK,i==3)
    text(c, 'Source: Leiber et al., “An Introductory Survey to Autoencoder-based Deep Clustering,” arXiv:2504.02087v2, 2025.', 82, 72, 1050, 14, MUTED)
    c.save()

if __name__ == '__main__':
    make_pdf()
