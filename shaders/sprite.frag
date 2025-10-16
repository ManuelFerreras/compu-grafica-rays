#version 330 core

in vec2 v_uv;
out vec4 fragColor;

uniform sampler2D u_tex;

void main() {
    vec3 col = texture(u_tex, v_uv).rgb;
    fragColor = vec4(col, 1.0);
}
