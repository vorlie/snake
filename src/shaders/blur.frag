#version 330
in vec2 v_uv;
uniform sampler2D tex;
uniform vec2 u_dir; // direction and texel offset
uniform float u_radius;
// multiplier to increase blur spread
out vec4 f_color;

// 9-tap Gaussian weights (5 unique symmetrical weights)
// These are normalized (sum to 1.0)
const float w[5] = float[](
    0.227027,  // w[0] (center)
    0.1945946, // w[1]
    0.1216216, // w[2]
    0.054054,  // w[3]
    0.016216   // w[4]
);

void main() {
    vec3 c = vec3(0.0);
    
    // We sample -4..4 using u_radius as multiplier for spacing
    for (int i = -4; i <= 4; ++i) {
        float weight = w[abs(i)];
        c += texture(tex, v_uv + u_dir * (float(i) * u_radius)).rgb * weight;
    }
    f_color = vec4(c, 1.0);
}