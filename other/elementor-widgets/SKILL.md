---
name: Elementor Widget Development
description: Expert knowledge in creating custom Elementor widgets with 3D integration, responsive controls, and SkyyRose branding. Triggers on keywords like "elementor", "widget", "elementor widget", "custom element", "elementor pro", "page builder".
version: 1.0.0
---

# Elementor Widget Development

Build custom Elementor widgets with advanced features including 3D viewers, luxury animations, and SkyyRose brand integration.

## When to Use This Skill

Activate when working on:
- Custom Elementor widget development
- 3D product viewer widgets
- Collection grid widgets
- Pre-order form widgets
- Luxury testimonial carousels
- Interactive product galleries
- Custom Elementor controls
- Widget responsive settings

## Widget Structure

### Basic Widget Class

```php
<?php
/**
 * SkyyRose Product 3D Viewer Widget
 *
 * @package SkyyRose_2025
 */

namespace SkyyRose\Elementor\Widgets;

use Elementor\Widget_Base;
use Elementor\Controls_Manager;
use Elementor\Group_Control_Typography;
use Elementor\Core\Schemes\Typography;

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

class Product_3D_Viewer extends Widget_Base {

    /**
     * Get widget name
     */
    public function get_name() {
        return 'skyyrose-3d-viewer';
    }

    /**
     * Get widget title
     */
    public function get_title() {
        return __('3D Product Viewer', 'skyyrose');
    }

    /**
     * Get widget icon
     */
    public function get_icon() {
        return 'eicon-3d-sphere';
    }

    /**
     * Get widget categories
     */
    public function get_categories() {
        return ['skyyrose'];
    }

    /**
     * Get widget keywords
     */
    public function get_keywords() {
        return ['3d', 'product', 'viewer', 'skyyrose', 'jewelry'];
    }

    /**
     * Register widget controls
     */
    protected function register_controls() {

        // Content Section
        $this->start_controls_section(
            'content_section',
            [
                'label' => __('3D Model', 'skyyrose'),
                'tab'   => Controls_Manager::TAB_CONTENT,
            ]
        );

        // Product selection
        $this->add_control(
            'product_id',
            [
                'label'       => __('Select Product', 'skyyrose'),
                'type'        => Controls_Manager::SELECT2,
                'options'     => $this->get_products(),
                'default'     => '',
                'label_block' => true,
            ]
        );

        // 3D Model URL
        $this->add_control(
            'model_url',
            [
                'label'       => __('3D Model URL (.gltf or .glb)', 'skyyrose'),
                'type'        => Controls_Manager::URL,
                'placeholder' => __('https://assets.skyyrose.co/models/product.glb', 'skyyrose'),
                'default'     => [
                    'url' => '',
                ],
            ]
        );

        // Auto-rotate
        $this->add_control(
            'auto_rotate',
            [
                'label'        => __('Auto Rotate', 'skyyrose'),
                'type'         => Controls_Manager::SWITCHER,
                'label_on'     => __('Yes', 'skyyrose'),
                'label_off'    => __('No', 'skyyrose'),
                'return_value' => 'yes',
                'default'      => 'yes',
            ]
        );

        // Camera position
        $this->add_control(
            'camera_position',
            [
                'label'   => __('Initial Camera Position', 'skyyrose'),
                'type'    => Controls_Manager::DIMENSIONS,
                'size_units' => ['px'],
                'default' => [
                    'top'    => 0,
                    'right'  => 0,
                    'bottom' => 5,
                    'left'   => 0,
                ],
            ]
        );

        $this->end_controls_section();

        // Style Section
        $this->start_controls_section(
            'style_section',
            [
                'label' => __('Viewer Style', 'skyyrose'),
                'tab'   => Controls_Manager::TAB_STYLE,
            ]
        );

        // Container height
        $this->add_responsive_control(
            'viewer_height',
            [
                'label'      => __('Height', 'skyyrose'),
                'type'       => Controls_Manager::SLIDER,
                'size_units' => ['px', 'vh'],
                'range'      => [
                    'px' => [
                        'min' => 300,
                        'max' => 1000,
                    ],
                    'vh' => [
                        'min' => 30,
                        'max' => 100,
                    ],
                ],
                'default'    => [
                    'unit' => 'px',
                    'size' => 600,
                ],
                'selectors'  => [
                    '{{WRAPPER}} .skyyrose-3d-viewer' => 'height: {{SIZE}}{{UNIT}};',
                ],
            ]
        );

        // Background color
        $this->add_control(
            'background_color',
            [
                'label'     => __('Background Color', 'skyyrose'),
                'type'      => Controls_Manager::COLOR,
                'default'   => '#F5F5F5',
                'selectors' => [
                    '{{WRAPPER}} .skyyrose-3d-viewer' => 'background-color: {{VALUE}};',
                ],
            ]
        );

        // Lighting preset
        $this->add_control(
            'lighting_preset',
            [
                'label'   => __('Lighting Preset', 'skyyrose'),
                'type'    => Controls_Manager::SELECT,
                'options' => [
                    'studio'  => __('Studio', 'skyyrose'),
                    'outdoor' => __('Outdoor', 'skyyrose'),
                    'luxury'  => __('Luxury (Rose Gold)', 'skyyrose'),
                    'dramatic' => __('Dramatic', 'skyyrose'),
                ],
                'default' => 'luxury',
            ]
        );

        $this->end_controls_section();

        // Controls Section
        $this->start_controls_section(
            'controls_section',
            [
                'label' => __('Viewer Controls', 'skyyrose'),
                'tab'   => Controls_Manager::TAB_CONTENT,
            ]
        );

        // Show controls
        $this->add_control(
            'show_controls',
            [
                'label'        => __('Show Controls', 'skyyrose'),
                'type'         => Controls_Manager::SWITCHER,
                'label_on'     => __('Yes', 'skyyrose'),
                'label_off'    => __('No', 'skyyrose'),
                'return_value' => 'yes',
                'default'      => 'yes',
            ]
        );

        // Zoom control
        $this->add_control(
            'enable_zoom',
            [
                'label'        => __('Enable Zoom', 'skyyrose'),
                'type'         => Controls_Manager::SWITCHER,
                'label_on'     => __('Yes', 'skyyrose'),
                'label_off'    => __('No', 'skyyrose'),
                'return_value' => 'yes',
                'default'      => 'yes',
                'condition'    => [
                    'show_controls' => 'yes',
                ],
            ]
        );

        // AR mode (future)
        $this->add_control(
            'enable_ar',
            [
                'label'        => __('Enable AR (Beta)', 'skyyrose'),
                'type'         => Controls_Manager::SWITCHER,
                'label_on'     => __('Yes', 'skyyrose'),
                'label_off'    => __('No', 'skyyrose'),
                'return_value' => 'yes',
                'default'      => 'no',
            ]
        );

        $this->end_controls_section();
    }

    /**
     * Get products for select dropdown
     */
    protected function get_products() {
        $products = [];

        $query = new \WP_Query([
            'post_type'      => 'product',
            'posts_per_page' => -1,
            'orderby'        => 'title',
            'order'          => 'ASC',
        ]);

        if ($query->have_posts()) {
            while ($query->have_posts()) {
                $query->the_post();
                $products[get_the_ID()] = get_the_title();
            }
            wp_reset_postdata();
        }

        return $products;
    }

    /**
     * Render widget output
     */
    protected function render() {
        $settings = $this->get_settings_for_display();

        $model_url = $settings['model_url']['url'] ?? '';
        $product_id = $settings['product_id'] ?? 0;

        // Get model URL from product if not set directly
        if (empty($model_url) && $product_id) {
            $model_url = get_post_meta($product_id, '_3d_model_url', true);
        }

        if (empty($model_url)) {
            if (\Elementor\Plugin::$instance->editor->is_edit_mode()) {
                echo '<div class="elementor-alert elementor-alert-warning">';
                echo __('Please select a product or provide a 3D model URL.', 'skyyrose');
                echo '</div>';
            }
            return;
        }

        // Enqueue Three.js
        wp_enqueue_script('threejs');
        wp_enqueue_script('gltf-loader');
        wp_enqueue_script('orbit-controls');
        wp_enqueue_script('skyyrose-3d-viewer');

        // Widget wrapper
        $this->add_render_attribute('wrapper', 'class', 'skyyrose-3d-viewer');
        $this->add_render_attribute('wrapper', 'data-model-url', esc_url($model_url));
        $this->add_render_attribute('wrapper', 'data-auto-rotate', $settings['auto_rotate']);
        $this->add_render_attribute('wrapper', 'data-lighting', $settings['lighting_preset']);
        $this->add_render_attribute('wrapper', 'data-enable-zoom', $settings['enable_zoom']);
        $this->add_render_attribute('wrapper', 'data-enable-ar', $settings['enable_ar']);

        ?>
        <div <?php echo $this->get_render_attribute_string('wrapper'); ?>>
            <canvas class="viewer-canvas"></canvas>

            <?php if ($settings['show_controls'] === 'yes') : ?>
                <div class="viewer-controls">
                    <button class="control-btn" data-action="reset">
                        <span class="icon">↻</span>
                        <span class="sr-only"><?php _e('Reset View', 'skyyrose'); ?></span>
                    </button>

                    <?php if ($settings['enable_zoom'] === 'yes') : ?>
                        <button class="control-btn" data-action="zoom-in">
                            <span class="icon">+</span>
                            <span class="sr-only"><?php _e('Zoom In', 'skyyrose'); ?></span>
                        </button>
                        <button class="control-btn" data-action="zoom-out">
                            <span class="icon">-</span>
                            <span class="sr-only"><?php _e('Zoom Out', 'skyyrose'); ?></span>
                        </button>
                    <?php endif; ?>

                    <?php if ($settings['enable_ar'] === 'yes') : ?>
                        <button class="control-btn control-ar" data-action="ar">
                            <span class="icon">📱</span>
                            <span class="label"><?php _e('View in AR', 'skyyrose'); ?></span>
                        </button>
                    <?php endif; ?>
                </div>
            <?php endif; ?>

            <div class="viewer-loading">
                <div class="spinner"></div>
                <p><?php _e('Loading 3D model...', 'skyyrose'); ?></p>
            </div>
        </div>
        <?php
    }

    /**
     * Render widget output in the editor
     */
    protected function content_template() {
        ?>
        <#
        var modelUrl = settings.model_url.url || '';

        if (!modelUrl) {
            #>
            <div class="elementor-alert elementor-alert-warning">
                {{{ '<?php _e("Please select a product or provide a 3D model URL.", "skyyrose"); ?>' }}}
            </div>
            <#
            return;
        }
        #>

        <div class="skyyrose-3d-viewer"
             data-model-url="{{ modelUrl }}"
             data-auto-rotate="{{ settings.auto_rotate }}"
             data-lighting="{{ settings.lighting_preset }}">

            <canvas class="viewer-canvas"></canvas>

            <# if (settings.show_controls === 'yes') { #>
                <div class="viewer-controls">
                    <button class="control-btn" data-action="reset">↻</button>
                    <# if (settings.enable_zoom === 'yes') { #>
                        <button class="control-btn" data-action="zoom-in">+</button>
                        <button class="control-btn" data-action="zoom-out">-</button>
                    <# } #>
                </div>
            <# } #>
        </div>
        <?php
    }
}
```

## Widget Registration

### Register Custom Category

```php
<?php
/**
 * Register SkyyRose Elementor category
 */
add_action('elementor/elements/categories_registered', 'skyyrose_register_elementor_category');

function skyyrose_register_elementor_category($elements_manager) {
    $elements_manager->add_category(
        'skyyrose',
        [
            'title' => __('SkyyRose', 'skyyrose'),
            'icon'  => 'fa fa-gem',
        ]
    );
}
```

### Register Widgets

```php
<?php
/**
 * Register SkyyRose Elementor widgets
 */
add_action('elementor/widgets/register', 'skyyrose_register_elementor_widgets');

function skyyrose_register_elementor_widgets($widgets_manager) {

    require_once SKYYROSE_THEME_DIR . '/elementor-widgets/product-3d-viewer.php';
    require_once SKYYROSE_THEME_DIR . '/elementor-widgets/collection-grid.php';
    require_once SKYYROSE_THEME_DIR . '/elementor-widgets/pre-order-form.php';

    $widgets_manager->register(new \SkyyRose\Elementor\Widgets\Product_3D_Viewer());
    $widgets_manager->register(new \SkyyRose\Elementor\Widgets\Collection_Grid());
    $widgets_manager->register(new \SkyyRose\Elementor\Widgets\Pre_Order_Form());
}
```

## Advanced Widget Examples

### Collection Grid Widget

```php
<?php
namespace SkyyRose\Elementor\Widgets;

class Collection_Grid extends \Elementor\Widget_Base {

    public function get_name() {
        return 'skyyrose-collection-grid';
    }

    public function get_title() {
        return __('Collection Grid', 'skyyrose');
    }

    protected function register_controls() {

        $this->start_controls_section(
            'query_section',
            [
                'label' => __('Query', 'skyyrose'),
            ]
        );

        // Collection selection
        $this->add_control(
            'collection',
            [
                'label'   => __('Collection', 'skyyrose'),
                'type'    => \Elementor\Controls_Manager::SELECT,
                'options' => [
                    'signature'   => __('Signature', 'skyyrose'),
                    'black_rose'  => __('Black Rose', 'skyyrose'),
                    'love_hurts'  => __('Love Hurts', 'skyyrose'),
                    'all'         => __('All Collections', 'skyyrose'),
                ],
                'default' => 'all',
            ]
        );

        // Number of products
        $this->add_control(
            'posts_per_page',
            [
                'label'   => __('Products to Show', 'skyyrose'),
                'type'    => \Elementor\Controls_Manager::NUMBER,
                'default' => 12,
                'min'     => 1,
                'max'     => 100,
            ]
        );

        // Order by
        $this->add_control(
            'orderby',
            [
                'label'   => __('Order By', 'skyyrose'),
                'type'    => \Elementor\Controls_Manager::SELECT,
                'options' => [
                    'date'       => __('Date', 'skyyrose'),
                    'price'      => __('Price', 'skyyrose'),
                    'popularity' => __('Popularity', 'skyyrose'),
                    'rating'     => __('Rating', 'skyyrose'),
                ],
                'default' => 'date',
            ]
        );

        $this->end_controls_section();

        // Layout section
        $this->start_controls_section(
            'layout_section',
            [
                'label' => __('Layout', 'skyyrose'),
            ]
        );

        // Columns
        $this->add_responsive_control(
            'columns',
            [
                'label'          => __('Columns', 'skyyrose'),
                'type'           => \Elementor\Controls_Manager::NUMBER,
                'desktop_default' => 3,
                'tablet_default'  => 2,
                'mobile_default'  => 1,
                'min'            => 1,
                'max'            => 6,
            ]
        );

        // Gap
        $this->add_responsive_control(
            'gap',
            [
                'label'      => __('Gap', 'skyyrose'),
                'type'       => \Elementor\Controls_Manager::SLIDER,
                'size_units' => ['px'],
                'range'      => [
                    'px' => [
                        'min' => 0,
                        'max' => 100,
                    ],
                ],
                'default'    => [
                    'size' => 30,
                ],
                'selectors'  => [
                    '{{WRAPPER}} .collection-grid' => 'gap: {{SIZE}}{{UNIT}};',
                ],
            ]
        );

        $this->end_controls_section();
    }

    protected function render() {
        $settings = $this->get_settings_for_display();

        $args = [
            'post_type'      => 'product',
            'posts_per_page' => $settings['posts_per_page'],
            'orderby'        => $settings['orderby'],
        ];

        // Filter by collection
        if ($settings['collection'] !== 'all') {
            $args['meta_query'] = [
                [
                    'key'   => '_skyyrose_collection',
                    'value' => $settings['collection'],
                ],
            ];
        }

        $query = new \WP_Query($args);

        if (!$query->have_posts()) {
            echo '<p>' . __('No products found.', 'skyyrose') . '</p>';
            return;
        }

        $columns = [
            'desktop' => $settings['columns'],
            'tablet'  => $settings['columns_tablet'] ?? 2,
            'mobile'  => $settings['columns_mobile'] ?? 1,
        ];

        ?>
        <div class="collection-grid"
             data-columns-desktop="<?php echo esc_attr($columns['desktop']); ?>"
             data-columns-tablet="<?php echo esc_attr($columns['tablet']); ?>"
             data-columns-mobile="<?php echo esc_attr($columns['mobile']); ?>">

            <?php while ($query->have_posts()) : $query->the_post(); ?>
                <?php wc_get_template_part('content', 'product'); ?>
            <?php endwhile; ?>

        </div>
        <?php

        wp_reset_postdata();
    }
}
```

## Custom Controls

### 3D Model Picker Control

```php
<?php
namespace SkyyRose\Elementor\Controls;

class Model_Picker extends \Elementor\Base_Data_Control {

    public function get_type() {
        return 'skyyrose-model-picker';
    }

    public function content_template() {
        ?>
        <div class="elementor-control-field">
            <label class="elementor-control-title">{{{ data.label }}}</label>
            <div class="elementor-control-input-wrapper">
                <button class="elementor-button" type="button">
                    <?php _e('Select 3D Model', 'skyyrose'); ?>
                </button>
                <input type="hidden" data-setting="{{ data.name }}" />
                <div class="model-preview"></div>
            </div>
        </div>
        <?php
    }

    public function enqueue() {
        wp_enqueue_script(
            'skyyrose-model-picker',
            SKYYROSE_THEME_URI . '/assets/js/elementor/model-picker.js',
            ['jquery'],
            SKYYROSE_VERSION
        );

        wp_enqueue_style(
            'skyyrose-model-picker',
            SKYYROSE_THEME_URI . '/assets/css/elementor/model-picker.css',
            [],
            SKYYROSE_VERSION
        );
    }
}
```

## Widget JavaScript

### 3D Viewer Init Script

```javascript
// assets/js/elementor/3d-viewer.js
(function($) {
    'use strict';

    class SkyyRose3DViewer {
        constructor(element) {
            this.$element = $(element);
            this.canvas = this.$element.find('.viewer-canvas')[0];
            this.modelUrl = this.$element.data('model-url');
            this.autoRotate = this.$element.data('auto-rotate') === 'yes';
            this.lighting = this.$element.data('lighting');

            this.init();
        }

        init() {
            // Initialize Three.js scene
            this.scene = new THREE.Scene();

            // Camera
            this.camera = new THREE.PerspectiveCamera(
                45,
                this.$element.width() / this.$element.height(),
                0.1,
                1000
            );
            this.camera.position.set(0, 0, 5);

            // Renderer
            this.renderer = new THREE.WebGLRenderer({
                canvas: this.canvas,
                antialias: true,
                alpha: true
            });
            this.renderer.setSize(this.$element.width(), this.$element.height());
            this.renderer.setPixelRatio(window.devicePixelRatio);

            // Controls
            this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
            this.controls.autoRotate = this.autoRotate;
            this.controls.autoRotateSpeed = 2.0;
            this.controls.enableDamping = true;

            // Lighting
            this.setupLighting(this.lighting);

            // Load model
            this.loadModel();

            // Bind events
            this.bindEvents();

            // Start animation
            this.animate();
        }

        setupLighting(preset) {
            if (preset === 'luxury') {
                // Rose gold lighting for SkyyRose
                const keyLight = new THREE.DirectionalLight(0xffd7b5, 1.5);
                keyLight.position.set(5, 5, 5);
                this.scene.add(keyLight);

                const fillLight = new THREE.DirectionalLight(0xB76E79, 0.8);
                fillLight.position.set(-5, 0, -5);
                this.scene.add(fillLight);

                const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
                this.scene.add(ambientLight);
            }
            // ... other lighting presets
        }

        loadModel() {
            const loader = new THREE.GLTFLoader();

            this.$element.addClass('loading');

            loader.load(
                this.modelUrl,
                (gltf) => {
                    this.model = gltf.scene;
                    this.scene.add(this.model);

                    // Center model
                    const box = new THREE.Box3().setFromObject(this.model);
                    const center = box.getCenter(new THREE.Vector3());
                    this.model.position.sub(center);

                    this.$element.removeClass('loading');
                },
                (progress) => {
                    const percent = (progress.loaded / progress.total) * 100;
                    this.$element.find('.viewer-loading p').text(`Loading... ${percent.toFixed(0)}%`);
                },
                (error) => {
                    console.error('Error loading 3D model:', error);
                    this.$element.removeClass('loading').addClass('error');
                }
            );
        }

        bindEvents() {
            // Control buttons
            this.$element.on('click', '.control-btn', (e) => {
                const action = $(e.currentTarget).data('action');
                this.handleControlAction(action);
            });

            // Resize
            $(window).on('resize', () => this.onResize());
        }

        handleControlAction(action) {
            switch (action) {
                case 'reset':
                    this.resetView();
                    break;
                case 'zoom-in':
                    this.camera.position.z -= 0.5;
                    break;
                case 'zoom-out':
                    this.camera.position.z += 0.5;
                    break;
                case 'ar':
                    this.launchAR();
                    break;
            }
        }

        resetView() {
            this.camera.position.set(0, 0, 5);
            this.controls.reset();
        }

        onResize() {
            this.camera.aspect = this.$element.width() / this.$element.height();
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(this.$element.width(), this.$element.height());
        }

        animate() {
            requestAnimationFrame(() => this.animate());

            this.controls.update();
            this.renderer.render(this.scene, this.camera);
        }

        launchAR() {
            // AR Quick Look (iOS) or WebXR
            if (window.WebXRManager) {
                // WebXR implementation
            } else {
                // AR Quick Look fallback
                const anchor = document.createElement('a');
                anchor.rel = 'ar';
                anchor.href = this.modelUrl.replace('.glb', '.usdz');
                anchor.click();
            }
        }
    }

    // Initialize on Elementor frontend
    $(window).on('elementor/frontend/init', function() {
        elementorFrontend.hooks.addAction('frontend/element_ready/skyyrose-3d-viewer.default', function($scope) {
            new SkyyRose3DViewer($scope.find('.skyyrose-3d-viewer'));
        });
    });

})(jQuery);
```

## SkyyRose Branding

### Widget Styles

```css
/* elementor-widgets/assets/style.css */

:root {
    --skyyrose-primary: #B76E79;
    --skyyrose-secondary: #2C2C2C;
}

.skyyrose-3d-viewer {
    position: relative;
    background: #F5F5F5;
    border-radius: 12px;
    overflow: hidden;
}

.viewer-controls {
    position: absolute;
    bottom: 20px;
    right: 20px;
    display: flex;
    gap: 8px;
}

.control-btn {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: var(--skyyrose-primary);
    color: white;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(183, 110, 121, 0.3);
}

.control-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(183, 110, 121, 0.5);
}

.viewer-loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
```

## References

See `references/` for:
- `elementor-api-reference.md` - Complete Elementor API docs
- `custom-controls-guide.md` - Building custom controls
- `widget-best-practices.md` - Widget optimization
- `3d-integration-patterns.md` - Three.js + Elementor

## Examples

See `examples/` for:
- `product-3d-viewer.php` - Complete 3D viewer widget
- `collection-grid.php` - Filterable product grid
- `pre-order-form.php` - Custom form widget
- `luxury-testimonials.php` - Testimonial carousel widget
