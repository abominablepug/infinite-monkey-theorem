<script lang="ts">
	import './global.css';

	let { children } = $props();
</script>

<svelte:head></svelte:head>
{@render children()}
<footer>
	<p>Copyright 2024</p>
</footer>
