FROM odoo:17.0

# Copy custom configuration file
COPY ./config/odoo.conf /etc/odoo/odoo.conf

# Copy custom addons
COPY ./addons /mnt/extra-addons

# Switch to root user temporarily to perform privileged operations
USER root

# Change ownership of the /mnt/extra-addons directory to the odoo user
RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo

# Expose Odoo port
EXPOSE 8069

CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
