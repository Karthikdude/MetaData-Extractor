import { gsap } from 'gsap';
import anime from 'animejs/lib/anime.es.js';
import * as THREE from 'three';
import $ from 'jquery';

// GSAP example animation
gsap.from(".header", { duration: 1, y: -100, opacity: 0 });

// Anime.js example animation
anime({
    targets: '.animate-me',
    translateX: 250,
    duration: 800,
    easing: 'easeInOutQuad'
});

// Three.js example setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

camera.position.z = 5;

function animate() {
    requestAnimationFrame(animate);
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
    renderer.render(scene, camera);
}
animate();
