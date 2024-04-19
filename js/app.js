function calcular(){
    x = document.getElementById("lado_x").value
    y = document.getElementById("lado_y").value
    a = document.getElementById("lado_a").value
    b = document.getElementById("lado_b").value

    fetch('/fCalcula?lado_a='+a+'&lado_b='+b+'&lado_x='+x+'&lado_y='+y,  {
      headers: {
          Accept: 'application/json',
      }
    }).then((response) => response.json())
      .then(res => {dibujarRespuesta(res, a, b, x, y)} )
}
function dibujarRespuesta(r, a, b, x, y){
res = JSON.parse(r)
a = a * 100
b = b * 100
x = x * 100
y = y * 100
cols= res.cols
colsResto= res.colsResto
filas= res.filas
filasResto= res.filasResto
orientacion=res.orientacion
//dibujo rectangulo contenedor
r1=rectangulo(x,y, 0, 0, 'black' )

ad = document.getElementById("areaDibujo")
while (ad.firstChild) {
ad.removeChild(ad.firstChild);
}
//dibujo rectangulo contenedor
ad = document.getElementById("areaDibujo")
ad.appendChild(r1)

//dibujo matriz en orientacion inicial
if (orientacion=='ab') {m1_ancho = a; m1_alto = b} else {m1_ancho = b; m1_alto = a}
if (m1_ancho<m1_alto) {m2_x_ini=0; m2_y_ini=m1_alto*filas} else {m2_x_ini= m1_ancho*cols; m2_y_ini=0}

for (let f= 0; f < filas; f++){
    for (let c= 0; c < cols; c++){
        r =rectangulo(m1_ancho,m1_alto, c*m1_ancho, f*m1_alto, 'red' )
        ad.appendChild(r)
    }    
}
//dibujo la matriz volteada si correspnde
for (let f= 0; f < filasResto; f++){
    for (let c= 0; c < colsResto; c++){
        r =rectangulo(m1_alto,m1_ancho, (c*m1_alto) + m2_x_ini, (f*m1_ancho)+m2_y_ini, 'green' )
        ad.appendChild(r)
    }       
}
}



function rectangulo(ancho, alto, pos_x, pos_y, color){
const SVG_NS = "http://www.w3.org/2000/svg";
let rect = document.createElementNS(SVG_NS, 'rect');
rect.setAttributeNS(null, 'x', pos_x)
rect.setAttributeNS(null, 'y', pos_y)
rect.setAttributeNS(null, 'width', ancho )
rect.setAttributeNS(null, 'height', alto )
rect.setAttributeNS(null, 'stroke', color)
rect.setAttributeNS(null, 'fill', "white")

return rect



}
