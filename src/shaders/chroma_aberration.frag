#version 330
in vec2 v_uv;
uniform sampler2D tex;
uniform vec2 u_resolution; // screen size in pixels (though not used for sampling here)
uniform float u_amount;     // Intensity of the effect
uniform float u_center_bias; // How much to keep the center clean (0.0=off, 1.0=full)
out vec4 f_color;

void main() {
    // 1. Calculate distance from screen center (0.5, 0.5)
    vec2 center = vec2(0.5, 0.5);
    vec2 delta_uv = v_uv - center;
    
    // Calculate falloff factor
    float d2 = dot(delta_uv, delta_uv); 
    
    // Scale the amount by the falloff and the user uniform
    float aberration_amount = u_amount * (1.0 - u_center_bias) + (u_amount * u_center_bias * d2);
    
    // 2. Calculate the required UV offset for each channel
    vec2 offset = delta_uv * aberration_amount;

    // 3. Sample the texture with offsets
    // Get the full color at the required offset for R
    vec3 col_R_offset = texture(tex, v_uv - offset).rgb;
    
    // Get the full color at the original UV for G
    vec3 col_G_offset = texture(tex, v_uv).rgb;
    
    // Get the full color at the required offset for B
    vec3 col_B_offset = texture(tex, v_uv + offset).rgb;

    // 4. Combine channels: take the R from R-offset, G from G-offset, B from B-offset
    float red = col_R_offset.r;
    float green = col_G_offset.g;
    float blue = col_B_offset.b;

    f_color = vec4(red, green, blue, 1.0);
}