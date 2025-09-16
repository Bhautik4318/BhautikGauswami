// Particles Configuration Helper
// Provides consistent particle behavior across themes

interface ParticlesConfig {
    particles: {
        number: { value: number; density: { enable: boolean; value_area: number } };
        color: { value: string };
        shape: { type: string; stroke: { width: number; color: string } };
        opacity: { value: number; random: boolean; anim: any };
        size: { value: number; random: boolean; anim: any };
        line_linked: { enable: boolean; distance: number; color: string; opacity: number; width: number };
        move: any;
    };
    interactivity: any;
    retina_detect: boolean;
}

export function getParticlesConfig(theme: 'dark' | 'light'): ParticlesConfig {
    const particleColor = theme === 'dark' ? '#ffffff' : '#000000';
    
    return {
        particles: {
            number: {
                value: 150,
                density: {
                    enable: true,
                    value_area: 800
                }
            },
            color: {
                value: particleColor
            },
            shape: {
                type: 'circle',
                stroke: {
                    width: 0,
                    color: particleColor
                }
            },
            opacity: {
                value: 0.6,
                random: true,
                anim: {
                    enable: true,
                    speed: 1.5,
                    opacity_min: 0.2,
                    sync: false
                }
            },
            size: {
                value: 3,
                random: true,
                anim: {
                    enable: true,
                    speed: 2,
                    size_min: 0.5,
                    sync: false
                }
            },
            line_linked: {
                enable: true,
                distance: 150,
                color: particleColor,
                opacity: 0.4,
                width: 1.5
            },
            move: {
                enable: true,
                speed: 5,
                direction: 'none',
                random: true,
                straight: false,
                out_mode: 'bounce',
                bounce: true,
                attract: {
                    enable: false,
                    rotateX: 600,
                    rotateY: 1200
                }
            }
        },
        interactivity: {
            detect_on: 'canvas',
            events: {
                onhover: {
                    enable: false
                },
                onclick: {
                    enable: true,
                    mode: 'push'
                },
                resize: true
            },
            modes: {
                push: {
                    particles_nb: 8
                }
            }
        },
        retina_detect: true
    };
}