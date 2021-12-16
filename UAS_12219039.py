#Febrian Jenetrius Naben
#12219039

from logging import PlaceHolder
import json
import plotly.express as px
import pandas as pd
import streamlit as st

# prosedur membaca isi file
filedata = pd.read_csv("produksi_minyak_mentah.csv")
with open('kode_negara_lengkap.json') as data_negara:
    negara = json.load(data_negara)
    data_negara.close()
    dict = []
    for i in negara:
        name = i.get('name')
        alpha3 = i.get('alpha-3')
        code = i.get('country-code')
        region = i.get('region')
        subregion = i.get('sub-region')
        dict.append([name, alpha3, code, region, subregion])

# Fungsi untuk mencari kode negara
def fungsi_kode(x, dictionary) :
    for i in dictionary :
        if x == i[1] :
            x_name = str(i[0])
            x_code = ("Kode Negara : " + i[2])
            x_reg = ("Region : " + i[3])
            x_subregion = ("Subregion : " + i[4])
            break
        else :
            x_name = ""
            x_code = ""
            x_reg = ""
            x_subregion = ""

    return x_name, x_code, x_reg, x_subregion

# Membuat konfigurasi website,main page dan membagi halaman menjadi 2 kolom
st.set_page_config(page_title="Data Produksi Minyak Mentah Dunia", page_icon="floppy_disk",layout="wide")
st.markdown("<h1 style='text-align: center; color: black;'>Data Produksi Minyak Mentah Dunia</h1>", unsafe_allow_html=True)

# Kolom informasi untuk Soal D
# Soal keseluruhan tahun
st.header(":page_facing_up: Informasi")
st.subheader("Keseluruhan Tahun")
kolom_a, kolom_b, kolom_c = st.columns(3)

## Mencari yang Terkecil
with kolom_b:
    st.warning('Jumlah Produksi Minyak Mentah Terkecil Keseluruhan Tahun')
    df1 = filedata.sort_values(by='produksi')
    df_filt = df1[df1['produksi'] != 0]
    terkecil = df_filt.nsmallest(1, 'produksi')
    x_min = terkecil.iloc[0, 0]
    x_prod = str(terkecil.iloc[0,2])
    min_nama,min_kode,min_reg,min_subreg = fungsi_kode(x_min, dict)
    st.write("###### Jumlah Produksi : " + x_prod)
    st.write(min_nama)
    st.write(min_kode)
    st.write(min_reg)
    st.write(min_subreg)
## mencari yang Terbesar
with kolom_a:
    st.info('Jumlah Produksi Minyak Mentah Terbesar Keseluruhan Tahun')
    df1 = filedata.sort_values(by='produksi')
    terbesar = df1.nlargest(1, 'produksi')
    x_max = terbesar.iloc[0, 0]
    x_prod = str(terbesar.iloc[0,2])
    max_nama,max_kode,max_reg,max_subreg = fungsi_kode(x_max, dict)
    st.write("###### Jumlah Produksi : " + x_prod)
    st.write(max_nama)
    st.write(max_kode)
    st.write(max_reg)
    st.write(max_subreg)

## produksi minyak mentah = 0
with kolom_c:
    st.success('Jumlah Produksi = 0 Keseluruhan Tahun')
    zero_filt = df1[df1['produksi'] == 0]
    zero_code = zero_filt['kode_negara'].tolist()
    zero_list = []
    for j in zero_code :
        for i in dict :
            if i[1] == j:
                zero_list.append([i[0], i[2], i[3], i[4]])
                break
    df_zero = pd.DataFrame(zero_list, columns=['Nama', 'Kode Negara', 'Region', 'Subregion'])
    df_zero = df_zero.drop_duplicates(subset=['Nama'])
    Index_blank=[''] * len(df_zero)
    df_zero.index=Index_blank
    with st.container():
        st.dataframe(df_zero)

st.write("")

# Soal per tahun
st.subheader("Produksi Minyak Mentah Per Tahun")
T = st.number_input("Tahun :", int(filedata.min(axis=0)['tahun']), int(filedata.max(axis=0)['tahun']))
data_year = filedata.query('tahun == @T')
kolom_d, kolom_e, kolom_f = st.columns(3)

## mencari yang Terbesar
with kolom_d:
    st.info("Jumlah Produksi Terbesar pada Tahun {namatahun}".format(namatahun = T))
    with st.expander("Lihat Informasi"):
        maxdata_year = data_year.nlargest(1, 'produksi')
        x_max = maxdata_year.iloc[0, 0]
        x_prod = str(maxdata_year.iloc[0,2])
        max_nama,max_kode,max_reg,max_subreg = fungsi_kode(x_max, dict)
        st.write("###### Jumlah Produksi : " + x_prod)
        st.write(max_nama)
        st.write(max_kode)
        st.write(max_reg)
        st.write(max_subreg)

##mencari yang Terkecil
with kolom_e :
    st.warning("Jumlah Produksi Terkecil pada Tahun {namatahun}".format(namatahun = T))
    with st.expander("Lihat Informasi"):
        data_yearfilt = data_year[data_year['produksi'] != 0]
        mindata_year = data_yearfilt.nsmallest(1, 'produksi')
        x_min = mindata_year.iloc[0, 0]
        x_prod = str(mindata_year.iloc[0,2])
        min_nama,min_kode,min_reg,min_subreg = fungsi_kode(x_min, dict)
        st.write("###### Jumlah Produksi : " + x_prod)
        st.write(min_nama)
        st.write(min_kode)
        st.write(min_reg)
        st.write(min_subreg)

## produksi minyak mentah = 0
with kolom_f :
    st.success("Jumlah Produksi = 0 pada Tahun {namatahun}".format(namatahun = T))
    with st.expander("Lihat Tabel"):
        zerofilter = data_year[data_year['produksi'] == 0]
        zerocodeb = zerofilter['kode_negara'].tolist()
        listzerodata_year = []
        for j in zerocodeb :
            for i in dict :
                if i[1] == j:
                    listzerodata_year.append([i[0], i[2], i[3], i[4]])
                    break
        df_zeroyd = pd.DataFrame(listzerodata_year, columns=['Nama', 'Kode Negara', 'Region', 'Subregion'])
        df_zeroyd = df_zeroyd.drop_duplicates(subset=['Nama'])
        Index_blank=[''] * len(df_zeroyd)
        df_zeroyd.index=Index_blank
        st.dataframe(df_zeroyd)

st.write("")
st.write("")
st.write("")

# Kolom grafik dan opsi grafik untuk Soal A, B, C
st.header(":bar_chart: Grafik")
opt = ["Bar", "Line", "Scatter"]

# Soal A
st.markdown("#### Grafik Produksi Minyak Mentah Suatu Negara")
cntry = st.selectbox("Negara : ", options=(i[0] for i in dict), key="soala")
type_chart = st.selectbox("Tipe Grafik : ", options=opt, key="soalaa")
for i in dict:
        if i[0] == cntry :
            code = i[1]
if not((filedata['kode_negara'] == code).any()) :
    st.error("Tidak ada data produksi minyak mentah " + cntry)
else :
    with st.expander("Lihat Grafik"):
        soala_selection = filedata.loc[filedata["kode_negara"] == code]
        if type_chart == "Bar":
            barchart = px.bar(soala_selection, x = "tahun", y = "produksi", labels={'tahun' : 'Tahun', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, hover_data=['kode_negara'], title='Grafik Produksi Minyak Mentah {negara}'.format(negara=cntry), template="seaborn")
            st.plotly_chart(barchart, use_container_width=True)
        elif type_chart == "Scatter" :
            scatterchart = px.scatter(soala_selection, x = "tahun", y = "produksi", labels={'tahun' : 'Tahun', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, hover_data=['kode_negara'], title='Grafik Produksi Minyak Mentah {negara}'.format(negara=cntry), template="seaborn")
            st.plotly_chart(scatterchart, use_container_width=True)
        else :
            linechart = px.line(soala_selection, x = "tahun", y = "produksi", labels={'tahun' : 'Tahun', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, hover_data=['kode_negara'], title='Grafik Produksi Minyak Mentah {negara}'.format(negara=cntry), template="seaborn")
            st.plotly_chart(linechart, use_container_width=True)
st.write("")
st.write("")

# Soal B
st.markdown("#### Grafik B-Buah Negara dengan Jumlah Produksi Terbesar per Tahun")
year = st.number_input("Tahun : ", int(filedata.min(axis=0)['tahun']), int(filedata.max(axis=0)['tahun']), key="soalb")
ydata = filedata.query('tahun == @year')
b = (st.slider('Jumlah Negara Terbesar : ', 1, ydata['kode_negara'].nunique(), key="soalbb"))
cydata = ydata.nlargest(int(b), 'produksi')
type_chartb = st.selectbox("Tipe Grafik : ", options=opt, key="soalbbb")
judul = "Grafik {jumlah} Buah Negara dengan Jumlah Produksi Terbesar pada Tahun {tahunnya}".format(jumlah = b, tahunnya = year)
with st.expander("Lihat Grafik"):
    if type_chartb == "Bar":
        barchartb = px.bar(cydata, x = "kode_negara", y = "produksi", labels={'tahun' : 'Tahun', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, hover_data=['kode_negara'], title=judul, template="seaborn")
        st.plotly_chart(barchartb, use_container_width=True)
    elif type_chartb == "Scatter" :
        scatterchartb = px.scatter(cydata, x = "kode_negara", y = "produksi", labels={'tahun' : 'Tahun', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, hover_data=['kode_negara'], title=judul, template="seaborn")
        st.plotly_chart(scatterchartb, use_container_width=True)
    else :
        linechartb = px.line(cydata, x = "kode_negara", y = "produksi", labels={'tahun' : 'Tahun', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, hover_data=['kode_negara'], title=judul, template="seaborn")
        st.plotly_chart(linechartb, use_container_width=True)
st.write("")
st.write("")

# Membuat Tabel Akumulatif / Tabel keseluruhan soal C
temp = filedata['kode_negara'].ne(filedata['kode_negara'].shift()).cumsum()
filedata['kumulatif'] = filedata.groupby(temp)['produksi'].cumsum()
cumdata = filedata[['kode_negara', 'produksi', 'kumulatif']]
cumdata = cumdata.sort_values('kumulatif', ascending=False).drop_duplicates(subset=['kode_negara'])

st.markdown("#### Grafik B-Buah Negara dengan Jumlah Produksi Kumulatif Terbesar")
c = int(st.slider('Jumlah Negara Terbesar : ', 1, cumdata['kode_negara'].nunique(), key="soalc"))
cdata = cumdata.nlargest(c, 'kumulatif')
type_chartc = st.selectbox("Tipe Grafik : ", options=opt, key="soalcc")
with st.expander("Lihat Grafik"):
    if type_chartc == "Bar":
        barchartc = px.bar(cdata, x = "kode_negara", y = "kumulatif", labels={'kumulatif' : 'Jumlah Kumulatif', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, title="Grafik {jumlahngr} Buah Negara dengan Jumlah Kumulatif Produksi Terbesar".format(jumlahngr = c), template="seaborn")
        st.plotly_chart(barchartc, use_container_width=True)
    elif type_chartc == "Scatter" :
        scatterchartc = px.scatter(cdata, x = "kode_negara", y = "kumulatif", labels={'kumulatif' : 'Jumlah Kumulatif', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, title="Grafik {jumlahngr} Buah Negara dengan Jumlah Kumulatif Produksi Terbesar".format(jumlahngr = c), template="seaborn")
        st.plotly_chart(scatterchartc, use_container_width=True)
    else :
        linechartc = px.line(cdata, x = "kode_negara", y = "kumulatif", labels={'kumulatif' : 'Jumlah Kumulatif', 'produksi' : 'Jumlah Produksi', 'kode_negara' : 'Kode Negara'}, title="Grafik {jumlahngr} Buah Negara dengan Jumlah Kumulatif Produksi Terbesar".format(jumlahngr = c), template="seaborn")
        st.plotly_chart(linechartc, use_container_width=True)
