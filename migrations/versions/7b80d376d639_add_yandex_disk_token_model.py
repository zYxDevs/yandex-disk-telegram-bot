"""Add yandex disk token model

Revision ID: 7b80d376d639
Revises: e132de254282
Create Date: 2020-03-29 13:10:24.265810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b80d376d639'
down_revision = 'e132de254282'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('yandex_disk_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.String(), nullable=True, comment='Encrypted Y.D. OAuth token'),
    sa.Column('access_token_type', sa.String(), nullable=True, comment='Type of access token'),
    sa.Column('access_token_expires_in', sa.DateTime(), nullable=True, comment='Access token expires at this date (UTC+0)'),
    sa.Column('refresh_token', sa.String(), nullable=True, comment='Encrypted Y.D. refresh token to use to update access token'),
    sa.Column('insert_token', sa.String(), nullable=True, comment="Encrypted token for DB update controlling. i.e., you shouldn't insert values if you don't know insert token"),
    sa.Column('insert_token_expires_in', sa.DateTime(), nullable=True, comment='Insert token expires on this date (UTC+0)'),
    sa.Column('user_id', sa.Integer(), nullable=False, comment='Tokens belongs to this user'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('yandex_disk_tokens')
    # ### end Alembic commands ###
