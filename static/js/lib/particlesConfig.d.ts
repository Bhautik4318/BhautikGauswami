interface ParticlesConfig {
    particles: {
        number: {
            value: number;
            density: {
                enable: boolean;
                value_area: number;
            };
        };
        color: {
            value: string;
        };
        shape: {
            type: string;
            stroke: {
                width: number;
                color: string;
            };
        };
        opacity: {
            value: number;
            random: boolean;
            anim: any;
        };
        size: {
            value: number;
            random: boolean;
            anim: any;
        };
        line_linked: {
            enable: boolean;
            distance: number;
            color: string;
            opacity: number;
            width: number;
        };
        move: any;
    };
    interactivity: any;
    retina_detect: boolean;
}
export declare function getParticlesConfig(theme: 'dark' | 'light'): ParticlesConfig;
export {};
