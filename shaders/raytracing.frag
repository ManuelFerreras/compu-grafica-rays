#version 330 core

in vec2 v_uv;
out vec4 fragColor;

// ---- Cámara / escena ----
uniform vec3  u_cam_pos;
uniform float u_fov_y;     // en grados
uniform float u_aspect;    // width/height
uniform mat4  u_inv_view;

// Cielo
uniform vec3 u_sky_top;
uniform vec3 u_sky_bottom;

// Objetos (hasta MAX_OBJECTS)
const int MAX_OBJECTS = 16;
uniform int  u_num_objs;
uniform mat4 u_model[MAX_OBJECTS];

// 🎨 Colores por objeto (vec4 para subir como bloque)
uniform vec4 u_color[MAX_OBJECTS];

// 💡 Luz direccional en mundo (normalizada)
uniform vec3 u_light_dir;

// ---------- helpers ----------
float slabIntersectAABB(vec3 o, vec3 d, vec3 bmin, vec3 bmax, out float tFar) {
    float tmin = -1e20;
    float tmax =  1e20;

    // X
    if (abs(d.x) < 1e-8) {
        if (o.x < bmin.x || o.x > bmax.x) { tFar = -1.0; return -1.0; }
    } else {
        float t1 = (bmin.x - o.x) / d.x;
        float t2 = (bmax.x - o.x) / d.x;
        float tn = min(t1, t2);
        float tf = max(t1, t2);
        tmin = max(tmin, tn);
        tmax = min(tmax, tf);
        if (tmin > tmax) { tFar = -1.0; return -1.0; }
    }
    // Y
    if (abs(d.y) < 1e-8) {
        if (o.y < bmin.y || o.y > bmax.y) { tFar = -1.0; return -1.0; }
    } else {
        float t1 = (bmin.y - o.y) / d.y;
        float t2 = (bmax.y - o.y) / d.y;
        float tn = min(t1, t2);
        float tf = max(t1, t2);
        tmin = max(tmin, tn);
        tmax = min(tmax, tf);
        if (tmin > tmax) { tFar = -1.0; return -1.0; }
    }
    // Z
    if (abs(d.z) < 1e-8) {
        if (o.z < bmin.z || o.z > bmax.z) { tFar = -1.0; return -1.0; }
    } else {
        float t1 = (bmin.z - o.z) / d.z;
        float t2 = (bmax.z - o.z) / d.z;
        float tn = min(t1, t2);
        float tf = max(t1, t2);
        tmin = max(tmin, tn);
        tmax = min(tmax, tf);
        if (tmin > tmax) { tFar = -1.0; return -1.0; }
    }

    if (tmax < 0.0) { tFar = -1.0; return -1.0; }
    tFar = tmax;
    return (tmin >= 0.0) ? tmin : tmax; // si arrancás dentro, devolvé tmax
}

vec3 skyColor(vec3 dir) {
    float h = clamp(dir.y * 0.5 + 0.5, 0.0, 1.0);
    return mix(u_sky_bottom, u_sky_top, h);
}

// ---------- main ----------
void main() {
    // 1) Dirección del rayo en espacio de cámara
    float tanHalfFov = tan(radians(u_fov_y) * 0.5);
    float x_ndc = 2.0 * v_uv.x - 1.0;
    float y_ndc = 2.0 * v_uv.y - 1.0;

    vec3 dir_cam = normalize(vec3(
        x_ndc * u_aspect * tanHalfFov,
        y_ndc * tanHalfFov,
        -1.0
    ));

    // 2) A mundo
    vec3 origin_world = u_cam_pos;
    vec3 dir_world = normalize(mat3(u_inv_view) * dir_cam);

    // 3) Intersección con OBBs
    float bestT = 1e20;
    int   bestIdx = -1;

    for (int i = 0; i < u_num_objs && i < MAX_OBJECTS; ++i) {
        mat4 M    = u_model[i];
        mat4 invM = inverse(M);

        vec4 oL4 = invM * vec4(origin_world, 1.0);
        vec3 oL  = oL4.xyz / oL4.w;

        vec4 pL4 = invM * vec4(origin_world + dir_world, 1.0);
        vec3 dL  = normalize(pL4.xyz / pL4.w - oL);

        float tFar;
        float tNear = slabIntersectAABB(oL, dL, vec3(-0.5), vec3(0.5), tFar);
        if (tNear >= 0.0) {
            vec3 hitLocal = oL + dL * tNear;
            vec3 hitWorld = (M * vec4(hitLocal, 1.0)).xyz;
            float tWorld  = dot(hitWorld - origin_world, dir_world);
            if (tWorld > 0.0 && tWorld < bestT) {
                bestT = tWorld;
                bestIdx = i;
            }
        }
    }

    // 4) Shading
    vec3 col;
    if (bestIdx >= 0) {
        // Recalcular normal local del objeto ganador y pasar a mundo
        int  i    = bestIdx;
        mat4 M    = u_model[i];
        mat4 invM = inverse(M);

        vec4 oL4 = invM * vec4(origin_world, 1.0);
        vec3 oL  = oL4.xyz / oL4.w;

        vec4 pL4 = invM * vec4(origin_world + dir_world, 1.0);
        vec3 dL  = normalize(pL4.xyz / pL4.w - oL);

        float tFar2;
        float tNear2 = slabIntersectAABB(oL, dL, vec3(-0.5), vec3(0.5), tFar2);
        vec3 hitLocal = oL + dL * tNear2;

        vec3 nL = vec3(0.0);
        float eps = 1e-3;
        if      (abs(hitLocal.x - 0.5) < eps) nL = vec3( 1, 0, 0);
        else if (abs(hitLocal.x + 0.5) < eps) nL = vec3(-1, 0, 0);
        else if (abs(hitLocal.y - 0.5) < eps) nL = vec3(0,  1, 0);
        else if (abs(hitLocal.y + 0.5) < eps) nL = vec3(0, -1, 0);
        else if (abs(hitLocal.z - 0.5) < eps) nL = vec3(0, 0,  1);
        else if (abs(hitLocal.z + 0.5) < eps) nL = vec3(0, 0, -1);

        vec3 nW = normalize(mat3(M) * nL);
        vec3 L  = normalize(u_light_dir);

        float diff = max(dot(nW, L), 0.0);
        vec3 base  = u_color[i].rgb;
        col = base * (0.25 + 0.75 * diff);   // 25% ambiente + 75% difuso
    } else {
        col = skyColor(dir_world);
    }

    fragColor = vec4(col, 1.0);
}
