import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.optimize import linprog

st.set_page_config(page_title='EQUITY360 | Veltrix',page_icon='⚖️',layout='wide')
st.markdown('''<style>.stApp{background:#f5f7fb;color:#14233b}h1,h2,h3{color:#14233b}.block-container{padding-top:1.4rem}.stMetric{background:white;padding:12px;border-radius:12px;border:1px solid #e2e8f0}div[data-testid="stSidebar"]{background:#101d35}div[data-testid="stSidebar"] *{color:#f8fafc}</style>''',unsafe_allow_html=True)
np.random.seed(29)
N=6500
levels=np.random.choice(['L1','L2','L3','L4','L5'],N,p=[.17,.28,.27,.19,.09]); loc=np.random.choice(['Pune','Mumbai','Gurugram','Dubai'],N,p=[.38,.28,.25,.09]); gender=np.random.choice(['Woman','Man'],N,p=[.38,.62]); tenure=np.random.randint(0,12,N)
base={'L1':5,'L2':8,'L3':13,'L4':21,'L5':34}; target=np.array([base[x] for x in levels]); premium=np.where(tenure<=1,1.24,1.0); pay=np.round(target*premium*np.where(gender=='Woman',.93,1)*np.random.lognormal(0,.16,N),2)
critical=np.random.choice(['Critical','Standard'],N,p=[.23,.77]); performance=np.random.choice(['Exceeds','Meets','Developing'],N,p=[.23,.63,.14]); df=pd.DataFrame({'Employee ID':[f'V-{i:05d}' for i in range(N)],'Level':levels,'Location':loc,'Gender':gender,'Tenure':tenure,'Current CTC (₹L)':pay,'Role criticality':critical,'Performance':performance})
reference=df.groupby(['Level','Location'])['Current CTC (₹L)'].transform('median'); df['Reference CTC (₹L)']=reference.round(2);df['Indicative gap (₹L)']=np.maximum(0,reference-pay).round(2)
# Case-wide 48 Cr correction is given; synthetic records are diagnostic illustrations, not reconstruction of actual payroll.
st.sidebar.markdown('## ⚖️ EQUITY360')
st.sidebar.caption('VELTRIX TECHNOLOGIES · HR DECISION INTELLIGENCE')
page=st.sidebar.radio('Workspace',['Executive Overview','Pay Equity Diagnostics','Budget Optimizer','Retention & Trust'])
st.sidebar.divider();st.sidebar.warning('DEMO / SYNTHETIC DATA. Case-wide figures are from the brief; employee-level records and segment results are simulated.')
st.title('EQUITY360')
st.caption('From payroll exposure to defensible pay decisions · Project REBUILD')
if page=='Executive Overview':
 a,b,c,d=st.columns(4);a.metric('Workforce','6,500');b.metric('Correction estimate','₹48 Cr');c.metric('Leadership trust','22%','−46 pp');d.metric('Annualised attrition','31%','+17 pp')
 st.subheader('The problem is structural, not merely a data breach')
 x,y=st.columns([1.2,1]);
 with x:
  st.markdown('#### Four connected failure points')
  for h,t in [('01 · Pay governance','Unpublished bands and discretionary offers'),('02 · Hiring premiums','30–50% premiums for new joiners'),('03 · Reward calibration','High performers receiving lower hikes'),('04 · Trust and accountability','Opaque decisions and weak manager explanations')]:st.info(f'**{h}** — {t}')
 with y:
  fig=px.bar(pd.DataFrame({'Indicator':['Viewed leak','Perceive unfair pay','Actively job seeking','Managers unable to explain pay'],'Share':[85,62,48,74]}),x='Share',y='Indicator',orientation='h',range_x=[0,100],text='Share',color_discrete_sequence=['#2563eb']);fig.update_layout(height=350,showlegend=False,yaxis_title=None,xaxis_title='% of surveyed group');st.plotly_chart(fig,use_container_width=True)
 st.success('Decision sequence: audit equity → ring-fence mandatory remedies → optimise discretionary corrections → monitor trust and attrition.')
elif page=='Pay Equity Diagnostics':
 st.subheader('Pay Equity Diagnostic Engine');st.caption('Synthetic payroll; no statistical claim about Veltrix individual employees.')
 a,b,c=st.columns(3);chosen_level=a.selectbox('Job level',['All']+sorted(df.Level.unique()));chosen_loc=b.selectbox('Location',['All']+sorted(df.Location.unique()));chosen_gender=c.selectbox('Gender',['All','Woman','Man']);f=df.copy()
 if chosen_level!='All':f=f[f.Level==chosen_level]
 if chosen_loc!='All':f=f[f.Location==chosen_loc]
 if chosen_gender!='All':f=f[f.Gender==chosen_gender]
 a,b,c=st.columns(3);a.metric('Records',f'{len(f):,}');b.metric('Indicative below-reference',f'{(f["Indicative gap (₹L)"]>0).mean()*100:.1f}%');c.metric('Synthetic total gaps',f'₹{f["Indicative gap (₹L)"].sum()/100:.1f} Cr')
 x,y=st.columns(2)
 with x:st.plotly_chart(px.box(f,x='Level',y='Current CTC (₹L)',color='Gender',points=False,title='CTC dispersion by job level'),use_container_width=True)
 with y:
  temp=f.groupby(['Level','Gender'],as_index=False)['Current CTC (₹L)'].median();st.plotly_chart(px.bar(temp,x='Level',y='Current CTC (₹L)',color='Gender',barmode='group',title='Median CTC by level and gender'),use_container_width=True)
 st.markdown('**Method note:** The reference is the median within each job level and location, not a legally established fair-pay benchmark. A real review must control for skills, scope, experience, location, performance and compensation components.')
 st.dataframe(f[['Employee ID','Level','Location','Gender','Tenure','Current CTC (₹L)','Reference CTC (₹L)','Indicative gap (₹L)']].head(150),use_container_width=True,hide_index=True)
elif page=='Budget Optimizer':
 st.subheader('Compensation Correction Optimizer')
 st.caption('Optimises illustrative discretionary correction categories after mandatory liabilities are ring-fenced. All category costs and weights below are assumptions.')
 budget=st.slider('Annualised incremental pay budget (₹ Cr)',6,48,12,1)
 mandatory=st.slider('Mandatory legally required correction reserve (₹ Cr, illustrative)',0,min(18,budget),6,1)
 st.write(f'**Discretionary allocation available:** ₹{budget-mandatory} Cr · **Unfunded estimated correction envelope:** ₹{48-budget} Cr')
 categories=['Tenured pay inversion','High-performer anomalies','Other structural compression'];caps=np.array([18.,12.,12.]);weights=np.array([1.0,.82,.58]);available=max(0,budget-mandatory)
 res=linprog(-weights,A_ub=[np.ones(3)],b_ub=[available],bounds=[(0,float(v)) for v in caps],method='highs');alloc=np.maximum(0,res.x) if res.success else np.zeros(3)
 chart=pd.DataFrame({'Category':categories,'Allocated (₹ Cr)':alloc,'Remaining (₹ Cr)':caps-alloc});fig=px.bar(chart,x='Category',y=['Allocated (₹ Cr)','Remaining (₹ Cr)'],barmode='stack',color_discrete_sequence=['#10b981','#dbe4f0'],title='Optimised illustrative allocation');st.plotly_chart(fig,use_container_width=True)
 a,b,c=st.columns(3);a.metric('Mandatory reserve',f'₹{mandatory} Cr');b.metric('Discretionary allocated',f'₹{alloc.sum():.1f} Cr');c.metric('Annualised remaining gap',f'₹{48-budget} Cr')
 st.dataframe(chart.style.format({'Allocated (₹ Cr)':'{:.1f}','Remaining (₹ Cr)':'{:.1f}'}),use_container_width=True,hide_index=True)
 st.warning('The solver maximises a weighted correction score under a budget constraint. It is NOT a validated fairness or attrition prediction. Mandatory remedies cannot be postponed merely to fit a discretionary budget. The ₹48 Cr figure is assumed to be an annualised run-rate requirement for this demo.')
 st.code('Maximise: 1.00×inversion + 0.82×performance + 0.58×compression\nSubject to: sum(discretionary corrections) ≤ budget − mandatory reserve\n0 ≤ correction[j] ≤ category cap[j]',language='text')
else:
 st.subheader('Critical Talent & Trust Command Centre');st.caption('Risk matrix is scenario-based; no employee-level predictive model has been trained.')
 a,b,c,d=st.columns(4);a.metric('Resignations in 14 days','220');b.metric('Mid-tenure share of exits','60%');c.metric('Active job search','48%');d.metric('Offer acceptance','41%')
 x,y=st.columns(2)
 with x:
  risk=pd.DataFrame({'Group':['Critical mid-tenure','Client-facing leads','High performers','New joiners','Other roles'],'Flight risk (assumed)':[82,78,66,52,43],'Delivery impact (assumed)':[90,98,72,48,30]});fig=px.scatter(risk,x='Flight risk (assumed)',y='Delivery impact (assumed)',text='Group',size=[30,25,20,18,16],range_x=[0,100],range_y=[0,110],title='Segment-level continuity priority');fig.update_traces(textposition='top center');st.plotly_chart(fig,use_container_width=True)
 with y:
  months=['Baseline','Day 90 target','Month 12 target'];trust=[22,40,60];fig=px.line(x=months,y=trust,markers=True,range_y=[0,100],title='Leadership trust recovery targets (illustrative)',labels={'x':'Milestone','y':'Trust (%)'});st.plotly_chart(fig,use_container_width=True)
 st.info('Interventions: confidential stay interviews; succession cover; manager conversation training; independent grievance review; transparent aggregate progress reporting.')
