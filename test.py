
import pandas as pd
import folium
from h3 import h3
import easygui as G
import branca


def Map_inforaddit(clusters, gridgroup):
    # Convert the clusters dictionary items to polygons and add them to the map

    for k, v in clusters.items():
        if (h3.h3_is_valid(k)):
            points = h3.h3_to_geo_boundary(k)
            # points = [p[::-1] for p in points]
            tooltip = "{0} accidents".format(v['count'])
            if (v['count'] >= 0 and v['count'] < 10):
                polygon = folium.vector_layers.Polygon(locations=points, tooltip=tooltip, fill=True,
                                                       color='lightsalmon', fill_opacity=0.4, weight=2, opacity=0.4)
            elif (v['count'] >= 10 and v['count'] < 100):
                polygon = folium.vector_layers.Polygon(locations=points, tooltip=tooltip, fill=True, color='coral',
                                                       fill_opacity=0.4, weight=2, opacity=0.4)
            elif (v['count'] >= 100 and v['count'] < 1000):
                polygon = folium.vector_layers.Polygon(locations=points, tooltip=tooltip, fill=True, color='tomato',
                                                       fill_opacity=0.4, weight=2, opacity=0.4)
            else:
                polygon = folium.vector_layers.Polygon(locations=points, tooltip=tooltip, fill=True, color='orangered',
                                                       fill_opacity=0.4, weight=2, opacity=0.4)
            polygon.add_to(gridgroup)

    return gridgroup
# GET poly
def h3topoly(data,h3_clusters,res):
    for index, row in data.iterrows():
        key = row['h3level'+str(res)]
        if key in h3_clusters:
            h3_clusters[key]["count"] += 1
        else:
            h3_clusters[key] = {"count": 1}
    return h3_clusters

def lat_lng_to_h3(row,res):
    return h3.geo_to_h3(row['Start_Lat'], row['Start_Lng'], res)


uk = pd.read_csv(G.enterbox("数据集的地址:"))
# uk = pd.read_csv(r"D:\data\UK_Accidents.csv")
start=int(G.enterbox("层级开始于:"))
end=int(G.enterbox("层级结束于:"))
d=start
uk_acc=pd.DataFrame()
while(d<=end):
    uk_acc["h3level"+str(d)]=uk.apply(lat_lng_to_h3,res=d, axis=1)
    d=d+1
d=start
map1 = folium.Map(zoom_start=12)
while(d<=end):
    k = dict()
    h3_clusters = h3topoly(uk_acc, k,res=d)
    group= folium.FeatureGroup(name="Resolution level "+str(d), control=True,show=(d==start))
    group= Map_inforaddit(h3_clusters, group)
    map1.add_child(group)
    d=d+1
folium.LayerControl().add_to(map1)

colorlist = ['lightsalmon','coral','tomato','orangered']
colorbar = branca.colormap.StepColormap(colorlist, index=[0,1,2,3],vmin = 0,vmax =4, caption= 'Number of accidents：10^x')
map1.add_child(colorbar)

# map1.save(r"D:\data\初始test.html")
map1.save(G.enterbox("保存的地址以及文件名:") + ".html")
G.msgbox(" 已成功生成地图！")



