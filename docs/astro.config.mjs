// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'Kimino',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/TheAhumMaitra/Kimino' }],
			sidebar: [
				{
					label: 'Documentation',
					items: [
						// Each item here is one entry in the navigation menu.
						{ label: 'Introduction', slug: 'guides/introduction' },
						{ label: 'Installation', slug: 'guides/installation' },
						{ label: 'Create GUI or TUI app entry', slug: 'guides/tui'}
					],
				}
			],
		}),
	],
});
