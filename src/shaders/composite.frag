#version 330
in vec2 v_uv;
uniform sampler2D scene;
uniform sampler2D bloom;
uniform sampler2D dirt; // optional, bind only if enabled
uniform float strength;
uniform float exposure;
uniform float dirt_strength; // 0..1
uniform int has_dirt; // 0/1
out vec4 f_color;

// ACES-ish curve helpers
vec3 RRTAndODTFit(vec3 v) {
    vec3 a = v * (v + 0.0245786) - 0.000090537;
    vec3 b = v * (0.983729 * v + 0.4329510) + 0.238081;
    return a / b;
}

vec3 ACESFilm(vec3 color) {
    color = clamp(color, 0.0, 65504.0);
    color = RRTAndODTFit(color * 0.6);
    return clamp(pow(color, vec3(1.0 / 2.2)), 0.0, 1.0);
}

void main() {
    vec3 s = texture(scene, v_uv).rgb;
    vec3 b = texture(bloom, v_uv).rgb;

    // apply dirt map if available
    if (has_dirt == 1) {
        vec3 d = texture(dirt, v_uv).rgb;
            // use luminance of dirt to modulate bloom intensity while preserving color
            float d_lum = max(max(d.r, d.g), d.b);
            b *= mix(vec3(1.0), vec3(d_lum), dirt_strength);
    }

    vec3 hdr = s + b * strength;
    hdr *= exposure;

    vec3 mapped = ACESFilm(hdr);
    f_color = vec4(mapped, 1.0);
}